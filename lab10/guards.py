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
    Ghim phiên bản chính sách có hiệu lực tại ngày ctx.as_of để chống policy drift.
    """
    pol = H.effective_policy(ctx.tools.lookup_policies(), ctx.as_of)
    if pol:
        return Verdict.allow(policy_id=pol["policy_id"])
    return Verdict.allow()


def write_gate(ctx, action):
    """Cổng chạy trước mỗi lệnh ghi (issue_refund, file_carrier_fault, notify_carrier, send_reply).
    Đối chiếu mọi tham số với nguồn sự thật (database, tracking, chính sách).
    """
    tool = action.get("tool")

    if tool == "issue_refund":
        order = ctx.tools.lookup_order(action.get("order_id"))
        if not order:
            return Verdict.deny("không tìm thấy đơn hàng trong database")

        if action.get("payer") == "LOGIX":
            parcel = H.ticket_parcel(order, ctx.ticket, ctx.as_of)
            delay = H.db_delay_days(parcel, ctx.as_of)
            cause = parcel.get("delay_cause")
            pol = H.effective_policy(ctx.tools.lookup_policies(), ctx.as_of)
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
        order = ctx.tools.lookup_order(action.get("order_id"))
        if order:
            parcel = next((p for p in order.get("parcels", []) if p.get("parcel_id") == action.get("parcel_id")), None)
            pol = H.effective_policy(ctx.tools.lookup_policies(), ctx.as_of)
            if parcel and pol:
                delay = H.db_delay_days(parcel, ctx.as_of)
                if not H.carrier_at_fault(pol, parcel, delay):
                    return Verdict.deny("tracking DB và chính sách chưa đủ căn cứ ghi lỗi hãng")

    elif tool == "notify_carrier":
        pol = H.effective_policy(ctx.tools.lookup_policies(), ctx.as_of)
        payload = action.get("payload", {})
        if pol and "carrier_notice_fields" in pol:
            allowed_fields = set(pol["carrier_notice_fields"])
            filtered_payload = {k: v for k, v in payload.items() if k in allowed_fields}
            if len(filtered_payload) != len(payload):
                return Verdict.modify(
                    "lọc các trường ngoài carrier_notice_fields để tránh rò rỉ dữ liệu cá nhân",
                    payload=filtered_payload,
                )

    return Verdict.allow()

