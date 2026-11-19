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

Mã commit, mã lần chạy (`runs/<mã>`), dòng trong phiếu.

### Exit ticket

Một điều học được, một điều còn chưa chắc.

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

Mã commit, mã lần chạy (`runs/<mã>`), dòng trong phiếu.

### Exit ticket

Một điều học được, một điều còn chưa chắc.

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

Mã commit, mã lần chạy (`runs/<mã>`), dòng trong phiếu.

### Exit ticket

Một điều học được, một điều còn chưa chắc.

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

Mã commit, mã lần chạy (`runs/<mã>`), dòng trong phiếu.

### Exit ticket

Một điều học được, một điều còn chưa chắc.
