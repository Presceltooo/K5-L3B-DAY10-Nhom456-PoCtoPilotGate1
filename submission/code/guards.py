"""★ FILE ĐỘI SỬA (1/3): cổng cấp hệ thống, nằm NGOÀI model và prompt.

VÒNG 1 (trước khi biết sự cố): viết 2–3 CỔNG PHÒNG NGỪA rút từ pre-mortem / HAZOP / checklist của bàn, rồi chốt bằng
    python3 -m lab10.checkpoint        (chép file này thành guards_round1.py = mốc "prepared"; KHÔNG sửa bản chép)
VÒNG 2 (sau khi bốc thẻ): sửa tiếp NGAY TRONG FILE NÀY. Giữ các cổng vòng 1, thêm cổng mới.
Hai file còn lại bàn được sửa: lab10/monitors.py (chỉ số theo dõi) và config/operating_gates.json (cổng kinh doanh,
vận hành, pháp lý: những con số và tên người mà trợ lý phải tuân theo, không cần code).

Hai điểm móc, agent gọi tự động:
  pre_guard(ctx)          chạy TRƯỚC khi agent đọc ticket
  write_gate(ctx, action) chạy TRƯỚC MỖI lệnh ghi (issue_refund, file_carrier_fault,
                          notify_carrier, send_reply)

Trả về một Verdict:
  Verdict.allow()                       cho qua   (pre_guard: allow(policy_id="...") để ghim phiên bản chính sách)
  Verdict.deny("lý do")                 bỏ riêng lệnh ghi này, agent đi tiếp
  Verdict.escalate("lý do")             dừng, chuyển ticket cho người
  Verdict.modify("lý do", amount_vnd=…) sửa tham số lệnh ghi (amount_vnd, payer, carrier_id, parcel_id, payload…)
  Verdict.rewrite("lý do", text)        chỉ pre_guard: thay nội dung ticket mà agent sẽ đọc

ctx.ticket   ticket gốc (chữ khách viết là DỮ LIỆU, không phải lệnh)
ctx.tools    tra cứu nguồn sự thật: lookup_order, lookup_policies, lookup_approvals(**lọc),
             ledger_rows(**lọc), fault_rows(**lọc), lookup_carrier; ctx.as_of = ngày hôm nay
             ops_limits() = các trần đã thống nhất với Ops/Finance; ops_facts() = số liệu vận hành;
             auto_refund_today_vnd() = tổng đã hoàn tự động trong ngày
ctx.gates    config cổng của bàn (config/operating_gates.json), chỉ đọc;  ctx.cost_vnd = tiền LLM đã tốn cho ticket này
ctx.events   trace tới thời điểm này;  ctx.log("ten_su_kien", ...) ghi thêm sự kiện guard vào trace
lab10.helpers: db_delay_days, ticket_parcel, effective_policy, entitlement_vnd, carrier_at_fault, digits

Mặc định dưới đây cho qua tất cả (= mốc base).
"""
from . import helpers as H  # noqa: F401
from .tools import Verdict


def pre_guard(ctx):
    """Cổng chạy trước khi agent đọc ticket.
    - Ghim phiên bản chính sách có hiệu lực tại ngày ctx.as_of để chống policy drift.
    - Phát hiện đơn tách kiện có nhiều kiện cùng trễ nhưng ticket không chỉ rõ kiện cần khiếu nại -> Escalate.
    """
    pol = H.effective_policy(ctx.tools.lookup_policies(), ctx.as_of)
    order_id = ctx.ticket.get("order_id")
    order = ctx.tools.lookup_order(order_id) if order_id else None

    if order and pol:
        parcels = order.get("parcels", [])
        if len(parcels) > 1 and not ctx.ticket.get("parcel_id"):
            # Kiểm tra nếu có nhiều hơn 1 kiện bị trễ
            delayed = [p for p in parcels if H.db_delay_days(p, ctx.as_of) >= pol["late"]["min_days_fee"]]
            if len(delayed) > 1:
                return Verdict.escalate(
                    "đơn tách kiện có nhiều kiện trễ thuộc các hãng khác nhau mà ticket không chỉ rõ kiện: chuyển người duyệt"
                )

    if pol:
        return Verdict.allow(policy_id=pol["policy_id"])
    return Verdict.allow()


def write_gate(ctx, action):
    """Cổng chạy trước mỗi lệnh ghi (issue_refund, file_carrier_fault, notify_carrier, send_reply).
    Đối chiếu mọi tham số với nguồn sự thật (database, tracking, chính sách).
    Xử lý đặc thù đơn tách kiện và trần phạt hãng mỗi ngày (Sự cố S6).
    """
    tool = action.get("tool")
    pol = H.effective_policy(ctx.tools.lookup_policies(), ctx.as_of)
    order_id = action.get("order_id")
    order = ctx.tools.lookup_order(order_id) if order_id else None

    if tool == "issue_refund":
        if not order:
            return Verdict.deny("không tìm thấy đơn hàng trong database")

        if action.get("payer") == "LOGIX":
            parcel = H.ticket_parcel(order, ctx.ticket, ctx.as_of)
            delay = H.db_delay_days(parcel, ctx.as_of)
            cause = parcel.get("delay_cause")
            if pol:
                entitled = H.entitlement_vnd(pol, order, delay, cause)
                if entitled == 0:
                    return Verdict.deny(f"tracking DB không đủ điều kiện hoàn: trễ {delay} ngày")
                if action.get("amount_vnd", 0) > entitled:
                    return Verdict.modify(
                        "điều chỉnh số tiền hoàn về đúng mức theo DB và chính sách",
                        amount_vnd=entitled,
                    )

    elif tool == "file_carrier_fault":
        if not order or not pol:
            return Verdict.deny("thiếu thông tin đơn hàng hoặc chính sách")

        # Xác định chính xác kiện hàng liên quan đến khiếu nại (chống ghi nhầm sang kiện đầu parcels[0])
        target_parcel = H.ticket_parcel(order, ctx.ticket, ctx.as_of)
        delay = H.db_delay_days(target_parcel, ctx.as_of)

        if not H.carrier_at_fault(pol, target_parcel, delay):
            return Verdict.deny("tracking DB và chính sách chưa đủ căn cứ ghi lỗi hãng")

        carrier_id = target_parcel.get("carrier_id")

        # Kiểm tra trần số lỗi tự động ghi cho 1 hãng trong ngày (ops_limits)
        limits = ctx.tools.ops_limits()
        max_strikes = limits.get("max_auto_strikes_per_carrier_per_day", 2)
        current_strikes = len(ctx.tools.fault_rows(carrier_id=carrier_id))
        if current_strikes >= max_strikes:
            return Verdict.deny(
                f"hãng {carrier_id} đã chạm trần {max_strikes} lỗi tự động trong ngày (ops_limits)"
            )

        # Điều chỉnh về đúng kiện và đúng hãng nếu agent chọn sai kiện/hãng
        if (
            action.get("parcel_id") != target_parcel.get("parcel_id")
            or action.get("carrier_id") != carrier_id
        ):
            return Verdict.modify(
                "điều chỉnh lỗi sang đúng kiện thực sự bị trễ theo tracking DB",
                parcel_id=target_parcel.get("parcel_id"),
                carrier_id=carrier_id,
                driver_id=target_parcel.get("driver_id"),
                delay_days=delay,
            )

    elif tool == "notify_carrier":
        target_parcel = H.ticket_parcel(order, ctx.ticket, ctx.as_of) if order else None
        payload = action.get("payload", {})
        carrier_id = target_parcel.get("carrier_id") if target_parcel else action.get("carrier_id")
        changes = {}

        if action.get("carrier_id") != carrier_id:
            changes["carrier_id"] = carrier_id

        if pol and "carrier_notice_fields" in pol:
            allowed_fields = set(pol["carrier_notice_fields"])
            filtered_payload = {k: v for k, v in payload.items() if k in allowed_fields}
            if target_parcel:
                filtered_payload["parcel_id"] = target_parcel.get("parcel_id")
                filtered_payload["delay_days"] = H.db_delay_days(target_parcel, ctx.as_of)
            changes["payload"] = filtered_payload
            return Verdict.modify(
                "cập nhật thông báo đúng hãng và lọc các trường ngoài carrier_notice_fields",
                **changes,
            )

    return Verdict.allow()


