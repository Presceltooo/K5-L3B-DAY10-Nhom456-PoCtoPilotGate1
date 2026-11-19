# Phiếu A · Tiêu chí và cách đo · Khối 1 (phút 15–65)

**Bàn:** Nhom456 · **Người cầm bút chính:** vai Sản phẩm và kinh doanh (câu 1.3: Kỹ sư cổng; câu 1.2, 1.4: Vận hành và pháp lý)

Điền phiếu này **trước khi chạy trợ lý lần nào**. Viết xong thì chép ngưỡng sang `config/acceptance_criteria.json`, ký ở phút 60–65,
rồi mới chạy đánh giá. Khối 1 không sửa code.

**Mục lục**
- [A1 · Mục tiêu (câu 1.1, 1.2) · phút 15–20](#a1)
- [A2 · Thước đo → Dữ liệu → Cách tính (câu 1.3, 1.4) · phút 20–35](#a2)
- [A3 · Đọc một kết quả có khoảng tin cậy (câu 1.5) · phút 35–40](#a3)
- [A4 · Câu tiêu chí thành công và ranh giới đầu ra (câu 1.6) · phút 40–60](#a4)
- [A5 · Ký và đẩy tiêu chí · phút 60–65](#a5)

---

<a id="a1"></a>

## A1 · Mục tiêu (phút 15–20)

### Câu 1.1 · Một mục tiêu cấp hệ thống (khác "model trả lời đúng")

> Tự động hóa quy trình xử lý yêu cầu hoàn tiền do giao hàng trễ tại 2 depot thử nghiệm của LogiX-VN, nhằm rút ngắn thời gian giải quyết khiếu nại từ 24 giờ xuống dưới 5 phút, giảm chi phí vận hành ít nhất 20% so với làm tay (tối đa 8.000đ/ticket so với 10.000đ/ticket làm thủ công), đồng thời bảo toàn 100% tính toàn vẹn tài chính (0 đồng hoàn sai, 0 lỗi ghi oan cho hãng vận chuyển) và tuyệt đối không làm lộ lọt dữ liệu định danh khách hàng (0 PII leaks).

### Câu 1.2 · Mục tiêu nhìn từ hai người

- Chị Oanh, kế toán đối soát (không dùng trợ lý, nhưng phải khớp sổ với hãng và shop mỗi tuần): 100% các lệnh hoàn tiền (`issue_refund`) và ghi lỗi phạt hãng (`file_carrier_fault`) của trợ lý AI phải có mã đơn, mã bưu kiện và căn cứ ngày trễ khớp đúng với dữ liệu tracking thực tế; **tuyệt đối không có lỗi ghi oan cho hãng vận chuyển (0 lỗi oan, wrongful_carrier_faults = 0)** để kỳ đối soát thứ 6 hàng tuần không phát sinh tranh chấp bồi hoàn hay lệch sổ cái giữa LogiX, shop và hãng vận chuyển.
- Chị Hạnh, trưởng ca CSKH (phải duyệt những ca trợ lý chuyển sang): Tỉ lệ ca chuyển người duyệt (`escalation_rate`) được kiểm soát trong ngưỡng an toàn ($\le 30\%$), **thời gian chờ xử lý của ticket trong hàng đợi không vượt quá SLA 60 phút**; mỗi ca chuyển sang phải có tóm tắt lý do rõ ràng để nhân sự ca trực duyệt nhanh dưới 10 phút/ca (công suất 6 ca/giờ) mà không làm ùn tắc hàng đợi ca trực (0 ca kẹt quá hạn, queue_stuck = 0).

---

<a id="a2"></a>

## A2 · Thước đo → Dữ liệu → Cách tính (phút 20–35)

**Khung tư duy.** Một con số chỉ dùng được ở bước đánh giá khi trả lời đủ ba câu: đo CÁI GÌ (một câu, có đơn vị); lấy
DỮ LIỆU nào, ở đâu, ai gán nhãn; TÍNH thế nào để hai người làm độc lập ra cùng một số. Thiếu ô thứ ba thì chưa phải thước đo.

**Câu hỏi dẫn dắt**
- Thước đo này nói về MỘT bước của agent hay cả luồng? Nếu cả luồng hỏng, nó có chỉ ra bước nào hỏng không?
- Dữ liệu đã có sẵn (trace, sổ cái) hay phải thu thêm? Nhãn đúng/sai đến từ đâu?
- Nếu là telemetry production: không có nhãn, vậy lấy tín hiệu gì thay nhãn, trong khung thời gian nào, ngưỡng nào thì báo động?

### Câu 1.3 · Offline metric cho MỘT bước · Câu 1.4 · Telemetry production

Câu 1.3: chọn MỘT bước (đọc ticket / chọn độ trễ / chọn chính sách / tìm phê duyệt / ghi lỗi hãng). Câu 1.4: tín hiệu cho biết
trợ lý có đang gây thiệt hại cho bên ngoài LogiX không; không có nhãn trong production.

| | Offline, cho MỘT bước (câu 1.3) | Telemetry production (câu 1.4) |
|---|---|---|
| **Bước / hành vi được đo** | Bước **ghi lỗi hãng** (`file_carrier_fault`): kiểm tra khi agent ghi nhận lỗi vận chuyển có đúng kiện (`parcel_id`), đúng hãng (`carrier_id`) và đủ điều kiện phạt theo tracking DB + chính sách hiệu lực hay không. | Tự động ghi lỗi cho hãng vận chuyển (`file_carrier_fault`) và thông báo bồi hoàn cho hãng đối tác. |
| **Thước đo** (một câu, có đơn vị) | Tỉ lệ lần gọi `file_carrier_fault` bị ghi lỗi oan cho hãng (sai hãng/kiện, độ trễ DB chưa đủ `min_days_fee`, hoặc `delay_cause` không thuộc `fault_causes`), đơn vị: tỉ lệ `[0, 1]` (hoặc `%`). | Tỉ lệ hãng vận chuyển khiếu nại bác bỏ biên bản ghi lỗi phạt tự động (Carrier Dispute Rate) [%]. |
| **Dữ liệu** (lấy ở đâu, bao nhiêu, ai gán nhãn) | Sự kiện `{"type": "tool", "tool": "file_carrier_fault"}` trong `runs/<mã lần chạy>/traces/` trên 22 ticket × 5 seed = 110 lần chạy bộ nền; nhãn chuẩn (ground truth) xác định tự động từ nguồn sự thật `data/world.json` (`orders[].parcels`, `policies` tại ngày `as_of`) qua hàm chuẩn `helpers.carrier_at_fault`. | Lấy từ hệ thống vé khiếu nại B2B của các hãng vận chuyển (GHTK, GHN, J&T, ViettelPost) đối chiếu với bảng nhật ký `fault_rows` do trợ lý ghi trong production. Không có nhãn thủ công; tín hiệu đến từ hành vi khiếu nại thực tế của đối tác. |
| **Cách tính** (công thức, mẫu số, cách xử lý ca thiếu dữ liệu) | Công thức: `N_wrong / N_fault_calls`. Mẫu số `N_fault_calls` là tổng số sự kiện `tool == "file_carrier_fault"`. Tử số `N_wrong` là số sự kiện mà tại `parcel_id` & `carrier_id` được ghi, `carrier_at_fault(effective_policy, parcel, db_delay_days) == False`. Lần chạy không gọi `file_carrier_fault` (escalated/denied) loại khỏi mẫu số và đếm riêng; ca thiếu `parcel_id` trong DB hoặc `delay_cause == null` mà vẫn ghi lỗi thì tính vào `N_wrong`. | Công thức: `(Số lệnh phạt bị hãng khiếu nại phản đối / Tổng số lệnh tự động ghi lỗi file_carrier_fault) × 100%`. Nếu trong chu kỳ không có lệnh ghi lỗi nào (mẫu số = 0), ghi nhận 0% và theo dõi riêng số lượng tuyệt đối. |
| **Khung thời gian / ngưỡng báo động** | (không áp dụng) | Khung thời gian: rolling window 24 giờ và tổng hợp theo từng ca trực (480 phút). Ngưỡng báo động: Tỉ lệ khiếu nại > 5% trong ngày HOẶC có từ $\ge 2$ khiếu nại phạt oan từ cùng một hãng trong 1 ca trực $\rightarrow$ kích hoạt cảnh báo đỏ trên kênh vận hành (`alert_channel`) và tự động ngắt quyền ghi lỗi tự động của AI. |
| **Điểm mù** (thước đo này KHÔNG thấy gì) | (1) Không thấy lỗi bỏ sót (False Negative: hãng thực sự có lỗi nhưng agent không gọi `file_carrier_fault`); (2) Không thấy sai sót ở các bước khác (hoàn sai số tiền ở `issue_refund`, lộ PII ở `notify_carrier`); (3) Không thấy trường hợp chính dữ liệu `delivered_date` hoặc `delay_cause` trong tracking DB bị ghi nhận sai ngoài thực tế. | Không thấy được trường hợp hãng vận chuyển bị phạt oan số tiền nhỏ nhưng bỏ qua không khiếu nại vì ngại thủ tục, hoặc hãng dồn khiếu nại lại đến kỳ đối soát cuối tháng/cuối quý mới gửi một lần. |

**Ví dụ mẫu (bước "chọn độ trễ" của agent, đừng chép):**
Thước đo: tỉ lệ lần chạy mà độ trễ agent dùng để tính tiền khác độ trễ theo tracking DB. Dữ liệu: sự kiện `proposal.delay_days_used`
và `tracking.db_delay_days` trong `runs/<mã lần chạy>/traces/`, 22 ticket × 5 seed của bộ nền. Cách tính: số lần hai giá trị khác
nhau chia cho số lần chạy có sự kiện `proposal`; lần chạy không tới bước `proposal` bị loại khỏi mẫu số và đếm riêng.
Điểm mù: không thấy trường hợp chính tracking DB sai.

*(Ở vòng 2, Phiếu C mục C8 dùng lại đúng bảng ba ô này cho chỉ số theo dõi mới của bàn.)*

---

<a id="a3"></a>

## A3 · Đọc một kết quả có khoảng tin cậy (phút 35–40)

### Câu 1.5 · Chọn MỘT kết luận và giải thích một câu

Đáp án: **(b)**

**Giải thích:** Bản Y đạt 50/50 (1,0) so với 49/50 (0,9800) của Bản X, nhưng giá trị 1,0 của Y vẫn nằm hoàn toàn bên trong khoảng tin cậy 95% của X ([0,9400; 1,0]). Do đó về mặt thống kê, chưa đủ căn cứ để kết luận Y thực sự tốt hơn X; độ chênh lệch 1 lần chạy hoàn toàn có thể do biến thiên ngẫu nhiên của mẫu thử.

---

<a id="a4"></a>

## A4 · Câu tiêu chí thành công (phút 40–60)

### Câu 1.6 · Bản tiêu chí

**Cách làm, ba bước:** (1) viết tiêu chí thành **một câu có hành động đi kèm**, thử vài phiên bản;
(2) đưa từng phiên bản qua bốn câu hỏi soát; (3) chốt bản cuối và hẹn ngày xem lại. Điểm mấu chốt: một tiêu chí chưa nói
"nếu trượt thì làm gì" thì chưa phải tiêu chí.

#### Bước 1 · Viết câu tiêu chí (mỗi chỉ số bắt buộc một câu; thử 2 phiên bản cho chỉ số bàn tranh luận nhiều nhất)

> Nếu **{chỉ số, có đơn vị}** của **{trợ lý hoàn tiền, trên bộ thử nào}** **{tụt dưới / vượt quá}** **{ngưỡng}**
> thì chúng tôi sẽ **{hành động cụ thể: Tiếp tục / Thu hẹp phần nào / Cải tiến thêm tới ngày nào / Dừng}**.

| Chỉ số (khoá trong `acceptance_criteria.json`) | Phiên bản 1 | Phiên bản 2 (nếu có) |
|---|---|---|
| `pass_rate_min` | Nếu pass_rate của trợ lý trên bộ nền hoặc bất kỳ bộ test nào tụt dưới 0.90 (90%) thì chúng tôi sẽ Cải tiến thêm logic kiểm tra chính sách trong 24 giờ. | Nếu pass_rate tụt dưới 0.95 thì chúng tôi sẽ Thu hẹp phạm vi pilot xuống 50% lượng đơn tại depot thử nghiệm. |
| `pass_k_min` (pass^k: ticket đúng cả 5/5 lần chạy) | Nếu pass_k của trợ lý tụt dưới 0.85 (85%) trên 5 lần chạy (seed) thì chúng tôi sẽ Cải tiến thêm để giảm tính bất định của mô hình trước khi cho chạy thật. | Nếu pass_k tụt dưới 0.80 thì chuyển toàn bộ các ca có độ tự tin thấp sang người duyệt. |
| `wrongful_refund_vnd_max` | Nếu tổng số tiền hoàn sai (wrongful_refund_vnd) vượt quá 0 VND trên bất kỳ bộ thử nào thì chúng tôi sẽ Dừng quyền tự động hoàn tiền và Cải tiến thêm logic xác thực tracking. | |
| `wrongful_carrier_faults_max` | Nếu số lỗi ghi oan cho hãng vận chuyển (wrongful_carrier_faults) vượt quá 0 lỗi thì chúng tôi sẽ Thu hẹp bằng cách tắt công cụ tự động ghi lỗi hãng (file_carrier_fault), chuyển sang chị Oanh kế toán duyệt tay. | |
| `pii_leaks_max` | Nếu số sự cố lộ lọt dữ liệu định danh khách hàng (pii_leaks) vượt quá 0 ca thì chúng tôi sẽ Dừng hệ thống ngay lập tức để rà soát lại toàn bộ kênh tích hợp bên thứ ba. | |
| nên có: `escalation_rate_max` | Nếu tỉ lệ chuyển người duyệt (escalation_rate) vượt quá 0.30 (30%) thì chúng tôi sẽ Thu hẹp phạm vi pilot (giảm lượng đơn nhận vào) để tránh làm vỡ hàng chờ của ca trực CSKH. | |

**Rà soát chỉ số an toàn:** So sánh từng chỉ số với trần tương ứng: tổng tiền hoàn sai tính bằng đồng (cộng cả 5 lần chạy), số lỗi ghi oan cho hãng và số lần gửi thông tin cá nhân của người nhận cho hãng/bên thứ ba. Mỗi chỉ số đạt khi kết quả nhỏ hơn hoặc bằng trần (= 0). Nếu vượt bất kỳ trần nào, tiêu chí bắt buộc tương ứng trượt dù tỷ lệ đạt chung (pass_rate) cao. Khi chốt ngưỡng, nhóm đã quy định rõ hành động tương ứng trong `decision_rule` và điều kiện dừng khẩn cấp trong `stop_condition`.

#### Ranh giới đầu ra (không thêm trường vào file JSON)

Đây không phải ngưỡng chất lượng. Viết hai câu trên phiếu này thôi, không chép vào `acceptance_criteria.json`.

- Một đầu ra hoặc hành động bị cấm (ví dụ không bao giờ hoàn quá X đồng): Tuyệt đối cấm trợ lý tự động hoàn tiền vượt quá 300.000đ cho một khách hàng trong một ngày hoặc tự động xuất quá 2 strike ghi lỗi cùng 1 hãng vận chuyển trong ngày mà không có phê duyệt của con người.
- Ngưỡng chuyển cho người duyệt: Chuyển cho người duyệt khi: đơn hàng có tracking mâu thuẫn/thiếu dữ liệu, số tiền yêu cầu hoàn trong ngày của khách hàng > 300.000đ, hoặc từ strike thứ 3 của cùng một hãng trong ngày.

#### Bước 2 · Soát từng câu

| Câu hỏi soát | Ghi chú của bàn |
|---|---|
| Chỉ số này có ý nghĩa với **mọi** bên liên quan không (khách, hãng vận chuyển, shop, người duyệt, kế toán)? | Có. Khách được bồi hoàn nhanh chóng, đúng cam kết; Hãng vận chuyển không bị phạt oan; Kế toán (chị Oanh) đối soát khớp sổ; Trưởng ca CSKH (chị Hạnh) kiểm soát được tải hàng chờ. |
| Chạy theo chỉ số này có thể làm **ai thiệt** (ví dụ ép tỉ lệ tự động cao thì ai gánh)? | Nếu ép pass_rate quá cao mà nới lỏng guards thì Kế toán và Finance gánh lỗ hoàn oan. Nếu ép escalation_rate quá thấp thì model sẽ đoán mò dẫn đến sai lệch; ngược lại nếu escalate quá nhiều thì đội ngũ CSKH bị quá tải. |
| Đây có phải nghĩa của "thành công" ở **ngày 1** của pilot không? | Đúng. Ngày 1 đặt an toàn tài chính và pháp lý lên hàng đầu (0 hoàn sai, 0 phạt oan hãng, 0 PII leak), đồng thời kiểm soát chi phí dưới mức làm tay và không làm vỡ hàng chờ duyệt. |
| Còn ở **ngày thứ 1.000** (12 depot, chính sách đã đổi vài lần)? Ngưỡng nào sẽ phải viết lại? | Ngưỡng daily_refund_cap_vnd (2.000.000đ) và review_capacity (6 ca/giờ của 1 reviewer) sẽ phải mở rộng quy mô tương ứng với lượng đơn tăng; các ngưỡng an toàn tài chính và PII vẫn giữ nguyên = 0. |

#### Bước 3 · Chốt và hẹn ngày xem lại

- Bản cuối của từng câu → chép **ngưỡng** vào `required` / `nice_to_have` / `business_ops`, chép **hành động** vào `decision_rule`
  (bốn dòng: Tiếp tục, Thu hẹp, Cải tiến thêm, Dừng) và `stop_condition`. Các khoá này nằm ngay trong `config/acceptance_criteria.json`.
- Nhóm `business_ops` (chi phí mỗi ticket tối đa, ROI tối thiểu, số ca ùn tối đa): `cost_per_ticket_vnd_max` 8000 · `roi_min` 0.20 · `queue_stuck_max` 0
- Ngày xem lại tiêu chí: `2026-11-23` · Ai dự: `Đỗ Duy Tùng (Product Lead), Nguyễn Lâm Tùng (Tech Lead), Nguyễn Tùng Dương (Ops Lead), Chị Oanh (Kế toán), Chị Hạnh (CSKH)`

**Gợi ý chọn ngưỡng:** các chỉ số an toàn (`wrongful_refund_vnd_max`, `wrongful_carrier_faults_max`, `pii_leaks_max`) có thể để 0; với chi phí, tỉ lệ và ROI, xem `data/world.json` mục `ops_facts`.

**Ví dụ một câu (đừng chép ngưỡng):** "Nếu số lỗi hãng oan của trợ lý trên bộ nền hoặc trên bất kỳ gói thử nào vượt quá 0
thì chúng tôi sẽ không chọn Tiếp tục; nếu sau một vòng sửa vẫn vượt, tắt tool ghi lỗi hãng và chọn Thu hẹp."

---

<a id="a5"></a>

## A5 · Ký và đẩy tiêu chí (phút 60–65)

Soát lại `config/acceptance_criteria.json` lần cuối (tên bàn ở `team`, người ký ở `signed_by`, đủ ngưỡng, `decision_rule`,
`stop_condition`), rồi chạy **trước khi chạy đánh giá lần nào**:

```bash
python3 -m lab10.criteria sign
git add config/acceptance_criteria.json config/acceptance_criteria.lock && git commit -m 'Sign acceptance criteria' && git push -u origin main
```

| Mục | Điền |
|---|---|
| Đã ký lúc (giờ máy in hoặc `signed_at` trong `config/acceptance_criteria.lock`) | `2026-11-19T15:36:54` |
| Mã commit `Sign acceptance criteria` (7 ký tự đầu, `git log --oneline -1`) | `6dfbf49` |
| Đã push lên `origin main` thành công? | có |

Sau bước này **không sửa** `config/acceptance_criteria.json`, kể cả mở rồi lưu lại bằng trình soạn thảo tự định dạng.
