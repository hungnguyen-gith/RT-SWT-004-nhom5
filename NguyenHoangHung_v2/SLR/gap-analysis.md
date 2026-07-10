# GAP Analysis – LLM for Unit Test Case Generation
Evidence table: N = 8 papers | Ngày: 2026-06-11

---

## Bảng GAP

| Tool/LLM | GAP-T | GAP-D | GAP-M | Hạn chế | GAP-S |
|---|---|---|---|---|---|
| GPT-3.5-turbo (HITS) | ✓ | – | – | – | ✓ |
| ChatGPT GPT-3 Jan 2023 (Tang et al.) | ✓ | – | – | – | ✓ |
| GPT-3.5 / GPT-4 / Mistral 7B / Mixtral 8x7B (Ouédraogo et al.) | ✓ | – | – | – | ✓ |
| CodeGen2 16B + GPT-4 (SymPrompt) | ✓ | ✓ | – | – | – |
| ChatGPT-3.5-turbo (Guerino & Vincenzi) | ✓ | ✓ | – | – | – |
| Mistral 7B (2SZSP) | ✓ | – | ✓ | – | – |
| GPT-4o + DeepSeek V3 (Cabral et al.) | ✓ | – | ✓ | – | ✓ |
| 12 SOTA LLMs (ULT Bench) | ✓ | ✓ | ✓ | – | ✓ |

---

## GAP Chính: GAP-T

**Phát biểu GAP-T (1–2 câu):**
Không có nghiên cứu nào trong 8 paper đánh giá GPT-4o mini (zero-shot) trực tiếp trên các function Java/Python có Cyclomatic Complexity trong khoảng 5–15 với so sánh đồng thời cả branch coverage ≥ 80% và mutation score ≥ 60% so với student-written tests và Randoop. Các nghiên cứu sử dụng GPT-4 (HITS, SymPrompt, Ouédraogo et al.) hoặc dùng framework phức tạp thêm (method slicing, AST traversal, CoT), hoặc không báo cáo mutation score, hoặc chỉ so sánh với EvoSuite/Pynguin chứ không so với Randoop hay student-written tests.

**Chi tiết kiểm tra bằng chứng – GAP-T Primary:**

| Tiêu chí | Mic/A/X | Ghi chú |
|---|---|---|
| Dataset | ✓ | CC 5–15 chưa được cô lập: HITS dùng CC > 10, ULT dùng CC ≥ 10; không paper nào cắt dải 5–15 |
| Tool/API | ✓ | GPT-4o mini zero-shot (không thêm framework) chưa được đánh giá độc lập |
| Compute | ✓ | CPU/Colab T4 đủ chạy |
| Ground truth | ✗ | Student-written tests chưa có sẵn; cần thu thập hoặc tạo mới |
| Skills | ✓ | Có thể thực hiện với kiến thức hiện có |
| Thời gian | ✓ | Trong vòng 1 tuần với buffer |

**Kết quả Feasibility Check:** 1× ✗ (Ground truth) → **Rủi ro cao – cần ghi amendment vào proposal trước khi commit.**

---

## GAP Secondary 1: GAP-D

**Phát biểu (1–2 câu):**
Không có dataset nào trong 8 paper cô lập chính xác dải Cyclomatic Complexity 5–15 cho cả Java lẫn Python trong một benchmark duy nhất. HITS dùng CC > 10 (Java), ULT Bench dùng CC ≥ 10 (Python), SymPrompt dùng các method Pynguin không thể cover (không filter theo CC cụ thể); không nghiên cứu nào có nhóm so sánh student-written tests ở cùng dải CC.

**Feasibility Check – GAP-D:**

| Tiêu chí | Mic/A/X | Ghi chú |
|---|---|---|
| Dataset | ⚠ | Có thể crawl GitHub; cần lọc theo CC bằng công cụ (Lizard, Radon) |
| Tool/API | ✓ | Không cần API đặc biệt |
| Compute | ✓ | CPU đủ |
| Ground truth | ✗ | Student-written tests chưa tồn tại; cần annotation |
| Skills | ✓ | Biết dùng Lizard/Radon |
| Thời gian | ⚠ | Thu thập + lọc + verify tốn > 1 tuần nếu làm từ đầu |

**Kết quả:** 1× ✗, 2× ⚠ → **Rủi ro cao – nên downscope hoặc ghép với GAP-T.**

---

## GAP Secondary 2: GAP-M

**Phát biểu (1–2 câu):**
Trong 8 paper, chỉ 3 paper báo cáo mutation score (Paper 5 – Guerino & Vincenzi dùng MutPy/Cosmic-Ray; Paper 6 – 2SZSP dùng JUGE; Paper 7 – Cabral et al. dùng PIT/Pitest); không paper nào kết hợp đồng thời mutation score và branch coverage ≥ 80% như một ngưỡng pass/fail kép. Đặc biệt không có paper nào so sánh mutation score của LLM-generated tests với student-written tests.

**Feasibility Check – GAP-M:**

| Tiêu chí | Mic/A/X | Ghi chú |
|---|---|---|
| Dataset | ✓ | Dùng lại dataset từ GAP-T/D |
| Tool/API | ✓ | PIT (Java) và Cosmic-Ray/MutPy (Python) đều free |
| Compute | ⚠ | Mutation testing tốn CPU; cần Colab T4 hoặc tương đương |
| Ground truth | ✗ | Vẫn phụ thuộc student-written tests (xem GAP-D) |
| Skills | ⚠ | Cần học thêm cách tích hợp PIT + pytest pipeline |
| Thời gian | ⚠ | Mutation testing chậm; buffer cần > 1 tuần du lịch |

**Kết quả:** 1× ✗, 3× ⚠ → **Rủi ro cao – chỉ viable khi GAP-T và GAP-D đã giải quyết xong.**

---

## GAP Secondary 3: GAP-S (Hạn chế chung)

**Phát biểu (1–2 câu):**
Năm trong số 8 paper chỉ đánh giá một ngôn ngữ (Java hoặc Python), không đánh giá cả hai; đồng thời không paper nào so sánh LLM-generated tests với Randoop (random test generation tool cho Java). Đây là giới hạn scope chung xuất hiện ở ít nhất 5/8 paper (Paper 1, 2, 3, 4, 6).

**Feasibility Check – GAP-S:**

| Tiêu chí | Mic/A/X | Ghi chú |
|---|---|---|
| Dataset | ✓ | Có thể reuse |
| Tool/API | ✓ | Randoop free, tích hợp JUnit |
| Compute | ✓ | CPU đủ |
| Ground truth | ⚠ | Randoop output là baseline; không cần annotation |
| Skills | ✓ | Randoop có tutorial |
| Thời gian | ✓ | Feasible trong 1 tuần |

**Kết quả:** 0× ✗, 1× ⚠ → **An toàn – có thể tích hợp vào RQ chính.**

---

## Tóm tắt GAP và ưu tiên

| GAP | Loại | Phát biểu 1 câu | Feasibility | Ưu tiên |
|---|---|---|---|---|
| GPT-4o mini zero-shot chưa được đánh giá độc lập trên CC 5–15 | GAP-T | Công nghệ/cách dùng chưa thử | Rủi ro cao (ground truth) | **Primary** |
| Không có dataset cô lập CC 5–15 kết hợp student tests | GAP-D | Domain/quy mô thiếu | Rủi ro cao | Secondary |
| Không paper nào kết hợp branch cov + mutation score như ngưỡng kép | GAP-M | Khía cạnh metric chưa đo | Rủi ro cao (phụ thuộc T+D) | Secondary |
| Không paper nào so Randoop; hầu hết chỉ 1 ngôn ngữ | GAP-S | Hạn chế chung của N = 5/8 paper | An toàn | Secondary |

**GAP primary được chọn: GAP-T** — ưu tiên cao nhất, pass feasibility tốt nhất sau khi giải quyết ground truth bằng amendment (thu thập student tests từ môn học lập trình trong trường).
