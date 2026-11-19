# Team

## Thông tin nhóm

- Tên nhóm: Nhom456
- Lớp: `L3B`
- Repo của bàn: `K5-L3B-DAY10-Nhom456-PoCtoPilotGate1`
- Thẻ sự cố đã bốc (S1–S8): *(Chờ bốc ở phút 125)*

## Thành viên

Họ tên đầy đủ và MSSV của **mọi** thành viên; bàn 3 người thì để trống dòng 4. Vai: Kỹ sư cổng · Sản phẩm và kinh doanh · Vận hành và pháp lý (README mục 3, phút 0–15).

| STT | Họ và tên | MSSV | Vai | Trưởng nhóm |
| --: | --------- | ---- | --- | :---------: |
|   1 | Đỗ Duy Tùng | 2A202603844 | Sản phẩm và kinh doanh | x |
|   2 | Nguyễn Lâm Tùng | 2A202603854 | Kỹ sư cổng | |
|   3 | Nguyễn Ngọc Vinh | 2A202603877 | Kỹ sư cổng | |
|   4 | Nguyễn Tùng Dương | 2A202603850 | Vận hành và pháp lý | |

Ghi `members` trong `submission/submission.json` theo dạng `"HoVaTen-MSSV"`, khớp bảng trên.

## Cá nhân

Mỗi thành viên tự viết một mục bên dưới (chép mẫu, đổi tiêu đề thành họ tên không dấu và MSSV, ví dụ `## NguyenVanAn-20241234`).

## DoDuyTung-2A202603844

### Phần việc phụ trách

Trưởng nhóm & Sản phẩm và kinh doanh.
- Quản trị repo, điều phối timeline, ký Bản tiêu chí và chốt các mốc Gate 1.
- Câu hỏi phụ trách: 1.1, 1.6 (Phiếu A: A1, A4); 2.3, 2.9 (Phiếu B: B3, B7.4); 3.2, 3.5 (Phiếu C: C5, C7); Quyết định v1 (B8) và Quyết định v2 (C12).
- File chính: `config/acceptance_criteria.json`, `config/operating_gates.json` (mục `business`), `submission/submission.json`.

### Đóng góp cụ thể

- Thiết lập repo nhóm, cấu hình thông tin thành viên.
- Xây dựng tiêu chí chấp nhận, thiết lập ngưỡng chi phí, ROI và quy tắc quyết định.
- Ký niêm phong tiêu chí và chốt checkpoint các vòng.
- Tổng hợp và hoàn thiện hồ sơ nộp bài.

### Bằng chứng

- Commit `6dfbf49`: `Sign acceptance criteria` (ký niêm phong `acceptance_criteria.json` với SHA-256 `4568068b`).
- Commit `7a137fa`: `LAB 10: chốt cổng vòng 1, quyết định v1` (chốt checkpoint snapshot `3fb56a01`).
- Báo cáo tự kiểm tra sự cố S6: `R-S6-grade-20261119-170200-82f3f8` (PASS-VISIBLE).
- File & Phiếu: `config/acceptance_criteria.json`, `config/acceptance_criteria.lock`, `templates/form-a-criteria.md` (mục A1 câu 1.1, A4 câu 1.6, A5), `templates/form-b-evaluation-gates.md` (mục B3 câu 2.3 bản đồ dữ liệu & phân tích drift, B7.4 câu 2.9 cổng kinh doanh, B8 quyết định v1), `templates/form-c-incident.md` (C5 câu 3.2, C7 câu 3.5, C12 quyết định v2), `submission/submission.json`.

### Exit ticket

- **Học được:** Hiểu rõ tầm quan trọng của việc đóng băng và niêm phong tiêu chí (`acceptance_criteria.lock`) trước khi chạy bất kỳ đánh giá nào để tránh thiên kiến "vẽ đường cho hươu chạy". Việc kiểm soát chi phí LLM, đặt trần hoàn tự động (`daily_refund_cap_vnd`) và trần lỗi phạt tự động của hãng xe (`max_auto_strikes_per_carrier_per_day`) là cốt lõi để bảo vệ an toàn tài chính và quan hệ đối tác kinh doanh.
- **Chưa chắc:** Phản ứng thực tế của mô hình và chi phí khi lưu lượng ticket bùng nổ gấp 3 lần trong các đợt sale lớn liệu có vượt quá dung lượng hàng đợi của nhân viên ca trực.

---

## NguyenLamTung-2A202603854

### Phần việc phụ trách

Kỹ sư cổng (Lead Gate Engineer).
- Phân tích trace log, thiết kế và cài đặt logic bảo vệ (guards) cho trợ lý AI.
- Câu hỏi phụ trách: 1.3 (Phiếu A: A2 cột Offline); 2.1, 2.2, 2.6, 2.7, 2.8 (Phiếu B: B1, B2, B7.1, B7.2, B7.3); 3.1, 3.5 (Phiếu C: C2, C7 code).
- File chính: `lab10/guards.py`.

### Đóng góp cụ thể

- Chạy các lượt đánh giá mốc base và sau khi dựng cổng.
- Viết các hàm chặn `pre_guard` và `write_gate` trong `lab10/guards.py`.
- Chuẩn bị behavioral test và 2 ticket hiểm test ad-hoc.
- Sửa cổng kỹ thuật khi gặp sự cố thẻ.

### Bằng chứng

- Commit `7a137fa`: `LAB 10: chốt cổng vòng 1, quyết định v1`.
- Lần chạy: `R-base-before-20261119-154553-b45eeb` (baseline), `R-base-after-20261119-164516-32d92f` (after đạt 110/110 pass), `R-base-prepared-20261119-164542-32d92f` (mốc prepared), `R-S6-after-20261119-165655-82f3f8` (after sự cố S6 đạt 60/60 pass).
- File & Phiếu: `lab10/guards.py`, `lab10/guards_round1.py`, `templates/form-a-criteria.md` (A2 offline metric), `templates/form-b-evaluation-gates.md` (B1 câu 2.1, B2 câu 2.2 bảng soát lỗi T-002@55, B7.1 câu 2.6 bảng 3 guards, B7.2 câu 2.7 tránh rò rỉ dữ liệu, B7.3 câu 2.8 behavioral tests), `templates/form-c-incident.md` (C2 bảng soát lỗi thẻ S6, C7 code bảo vệ đơn tách kiện và trần phạt hãng).

### Exit ticket

- **Học được:** Thay vì cố gắng sửa prompt của LLM để không tin lời khách, việc dựng một lớp chốt chặn hệ thống (`guards.write_gate`) độc lập với LLM đối chiếu trực tiếp với database tracking (`H.db_delay_days`, `H.entitlement_vnd`) là giải pháp an toàn tuyệt đối và có tính xác định cao. Trong xử lý đơn tách kiện, việc phân giải chính xác `target_parcel` thay vì lấy mặc định `parcels[0]` là chìa khóa để bảo vệ bên thứ ba khỏi bị phạt oan.
- **Chưa chắc:** Khi xuất hiện sự cố thẻ mới ngoài phân phối (ví dụ đứt gãy mạng lưới vận chuyển hoặc bão lũ), liệu logic `write_gate` hiện tại có đủ linh hoạt hay cần thêm các hook `pre_guard` can thiệp trước khi mô hình suy luận.

---

## NguyenNgocVinh-2A202603877

### Phần việc phụ trách

Kỹ sư cổng (QA & Telemetry Engineer).
- Đánh giá độ ổn định mô hình, kiểm tra regression và xây dựng hệ thống giám sát production.
- Câu hỏi phụ trách: 1.5 (Phiếu A: A3); 2.5 (Phiếu B: B6 - Pre-mortem); 3.4, 3.6, 3.7 (Phiếu C: C6, C8, C9).
- File chính: `lab10/monitors.py`.

### Đóng góp cụ thể

- Phân tích thống kê khoảng tin cậy cho pass rate.
- Xây dựng hàm giám sát mới trong `lab10/monitors.py`.
- Lập sơ đồ Fault Tree trước và sau khi xử lý sự cố.
- Kiểm thử đảm bảo không gây suy giảm chất lượng trên bộ test nền (No regression).

### Bằng chứng

- Commit `4146e58`: `docs(form-a): complete all sections of form A`.
- Commit `7a137fa`: `LAB 10: chốt cổng vòng 1, quyết định v1`.
- File & Phiếu: `lab10/monitors.py` (metric `split_order_fault_rate`), `templates/form-a-criteria.md` (A3 câu 1.5 đọc khoảng tin cậy thống kê CI 95% và phương án (b)), `templates/form-b-evaluation-gates.md` (B0 nhật ký 3 lần chạy, B6 câu 2.5 Pre-mortem 4 lăng kính), `templates/form-c-incident.md` (C6 Fault Tree trước sửa, C8 thiết kế metric mới, C9 Fault Tree sau sửa).

### Exit ticket

- **Học được:** Nhận thức sâu sắc rằng một pass_rate cao (như 99.09% ở baseline) hoàn toàn có thể che giấu những lỗi nghiêm trọng đối với bên thứ ba (hoàn sai tiền và phạt oan hãng ở `T-002@55`). Việc kiểm soát chặt chẽ pass^k, khoảng tin cậy và thiết kế các monitor nhạy bén như `split_order_fault_rate` giúp phát hiện bất thường ngay trong ca vận hành mà không cần nhãn kiểm thử.
- **Chưa chắc:** Cách thiết kế hàm giám sát telemetry realtime trong `monitors.py` sao cho vừa phát hiện sớm bất thường vừa không tạo ra quá nhiều báo động giả (false alarms) làm phiền đội ngũ vận hành.

---

## NguyenTungDuong-2A202603850

### Phần việc phụ trách

Vận hành và pháp lý (Ops & Legal Lead).
- Đảm bảo an toàn dữ liệu cá nhân (PII), quy trình phối hợp người - máy và pháp chế vận hành.
- Câu hỏi phụ trách: 1.2, 1.4 (Phiếu A: A1, A2 cột Telemetry); 2.4, 2.10 (Phiếu B: B4, B5, B7.5, B7.6); 3.1, 3.3, 3.7 (Phiếu C: C3, C4, C5, C10, C11).
- File chính: `config/operating_gates.json` (mục `operations` và `legal`).

### Đóng góp cụ thể

- Thiết kế chỉ số telemetry production theo dõi tác hại ngoại vi.
- Thực hiện HAZOP mở rộng và checklist 9 nhóm việc có phân công PIC rõ ràng.
- Thiết lập thông số vận hành (PIC, số ca trực, công suất duyệt) và chính sách PII.
- Xây dựng Runbook (phần 1–5), kịch bản ứng phó giờ cao điểm và cập nhật Risk Register.

### Bằng chứng

- Commit `4146e58`: `docs(form-a): complete all sections of form A`.
- Commit `7a137fa`: `LAB 10: chốt cổng vòng 1, quyết định v1`.
- File & Phiếu: `config/operating_gates.json` (mục `operations` và `legal`), `config/operating_gates.round1.json`, `templates/form-a-criteria.md` (A1 câu 1.2 góc nhìn chị Oanh/chị Hạnh, A2 telemetry production), `templates/form-b-evaluation-gates.md` (B4 câu 2.4 HAZOP vòng 1, B5 checklist 9 nhóm việc, B7.5 câu 2.10 Runbook 1-3, B7.6 quy trình giờ cao điểm), `templates/form-c-incident.md` (C3.2 hình dung con người vs hệ thống, C4 HAZOP thẻ S6, C5 giả định môi trường, C10 Risk Register, C11 Runbook 4-5).

### Exit ticket

- **Học được:** Một hệ thống AI vận hành an toàn không chỉ phụ thuộc vào code mà gắn liền mật thiết với quy trình con người và pháp lý: phải chỉ định rõ PIC, reviewer, hạn mức chờ hàng đợi (SLA 60 phút), cơ chế dừng khẩn cấp và bảo vệ dữ liệu cá nhân theo Nghị định 13 (lọc bỏ PII trước khi gửi sang hãng). Đồng thời, hợp đồng dịch vụ vận tải phải quy định rõ đơn vị chịu phạt là theo từng mã kiện thực tế thay vì tổng thể đơn hàng.
- **Chưa chắc:** Khi lượng ticket vào giờ cao điểm tăng đột biến, việc điều động reviewer dự phòng liệu có kịp thời để không làm vỡ cam kết thời gian chờ tối đa với khách hàng.

