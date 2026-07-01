# GAP Analysis — LLM for Unit Test Case Generation
**Thành viên:** Nguyễn Hữu Khánh Duy
Evidence table: N = 20 paper | Ngày: 02/06/2026

---

## Bảng GAP Tổng Hợp

| Cột | Phát hiện | Loại GAP | Phản chứng |
|-----|-----------|----------|------------|
| Tool/LLM | Không paper nào dùng **sinh viên đại học** (1–2 năm kinh nghiệm) làm nhóm C để so sánh với GPT-4 | GAP-T | ✅ Kiểm tra 20 paper — paper so sánh đều dùng developer hoặc "human-written" không xác định rõ |
| Metric | Không paper nào đo **đồng thời** branch coverage VÀ mutation score trên cùng bộ Java/Python medium CC (11–20) | GAP-M | ✅ Kiểm tra 20 paper — #9 chỉ đo branch; #10 chỉ đo mutation; #4 cảnh báo 2 metric không thay thế nhau |
| Dataset | Không có benchmark Python ở cyclomatic complexity **trung bình** (CC = 11–20) với mutation testing đầy đủ | GAP-D | ✅ Kiểm tra 20 paper — #8 (ULT) là benchmark Python duy nhất nhưng thiết kế với high CC |
| Hạn chế | "Dataset nhỏ / single CC level / không đo cả 2 metrics" được thừa nhận bởi ≥ 8/20 paper (= ceil(0.4×20)) | GAP-S | ✅ 8+ paper đều ghi hạn chế này trong Threats to Validity |

---

## GAP Chính: GAP-T + GAP-M
*(Ưu tiên theo thứ tự: GAP-T > GAP-M > GAP-D > GAP-S)*

**Lý do chọn GAP-T + GAP-M làm primary, không chọn GAP-D:**
GAP-D (thiếu benchmark Python medium CC) là vấn đề thực thi — có thể giải quyết bằng cách tự chọn/lọc hàm từ dataset public theo tiêu chí CC = 11–20 trong experiment design. GAP-T và GAP-M là khoảng trống **về câu hỏi nghiên cứu cốt lõi**: chưa ai so GPT-4 với sinh viên (không phải developer) và chưa ai đo đồng thời cả 2 ngưỡng chất lượng trên cùng bộ hàm. Đây là contribution khoa học, không phải vấn đề kỹ thuật.

**Phát biểu GAP Primary (dùng thẳng trong proposal):**
Chưa có nghiên cứu nào so sánh trực tiếp unit test do GPT-4 sinh ra với test do **sinh viên** viết thủ công, đồng thời đo cả branch coverage và mutation score trên cùng bộ Java/Python functions ở cyclomatic complexity trung bình (CC = 11–20).

## GAP Secondary 1: GAP-D

Không có benchmark Python nào được thiết kế với tiêu chí CC = 11–20 kèm mutation testing đầy đủ bằng MutPy. Paper gần nhất (#8, Huang 2025 ULT) chỉ bao gồm high CC functions. Nghiên cứu này giải quyết GAP-D bằng cách lọc dataset từ GitHub Python repos theo tiêu chí CC = 11–20 và chạy MutPy đầy đủ.

## GAP Secondary 2: GAP-S

Hạn chế "chỉ đo 1 metric" hoặc "không kiểm soát CC level" được thừa nhận bởi ≥ 8/20 paper, cho thấy đây là điểm yếu hệ thống. Paper #4 (Wang 2025) cảnh báo rõ: branch 100% nhưng mutation chỉ 4% — minh chứng hai metrics không thể thay thế nhau và phải đo đồng thời.

---

## Chi tiết kiểm tra phản chứng

### GAP-T: Chưa có paper nào dùng sinh viên (1–2 năm) làm nhóm C

| Paper | Nhóm C là ai? | Có phải sinh viên? | Ghi chú |
|-------|--------------|-------------------|---------|
| Yuan et al. 2024 (#1) | 5 Java developers | Không | Developer chuyên nghiệp, không phải sinh viên |
| Pan et al. 2024 (#6) | Developer-written tests | Không | Không xác định level; ngầm hiểu là developer |
| AgoneTest 2025 (#13) | "Human-written" | Không rõ | Không xác định rõ là developer hay sinh viên |
| Schäfer et al. 2024 (#4 IEEE TSE) | Developer-written | Không | Developer từ open-source projects |
| Guilherme & Vincenzi 2023 (#2) | Không so sánh human | Không áp dụng | Chỉ so với EvoSuite |
| Wang et al. 2024 (#3 ACM FSE) | Developer-written | Không | Open-source contributors |
| Pizzorno et al. 2025 (#16) | Không so sánh human | Không áp dụng | So SBST vs LLM, không có human group |
| ULT Benchmark 2025 (#8) | Không so sánh human | Không áp dụng | Benchmark only, không có human baseline |
| MDPI 2025 (#9) | Không so sánh human | Không áp dụng | Chỉ đo coverage tự động |
| Cabral 2025 (#10) | Không so sánh human | Không áp dụng | Chỉ đo mutation score |
| Seed&Steer 2025 (#21) | Không so sánh human | Không áp dụng | Chỉ đo branch coverage |
| Foster et al. 2025 (#8 Meta) | Meta engineers | Không | Senior engineers, không phải sinh viên |
| Tian et al. 2026 (#10 ProjectTest) | Không so sánh human | Không áp dụng | Benchmark project-level |
| ChatUniTest 2024 (#26) | Developer-written | Không | Developer từ open-source |
| Bhatia et al. 2024 (#27) | Developer-written | Không | Comparative performance, không sinh viên |
| Walczak et al. 2025 (#19) | Không so sánh human | Không áp dụng | Chỉ nghiên cứu prompting strategies |
| Rodriguez et al. 2025 (#20) | Không so sánh human | Không áp dụng | Equivalence partitioning study |
| MutGen 2025 (#28) | Không so sánh human | Không áp dụng | Mutation-guided generation |
| EvoGPT 2025 (#29) | Không so sánh human | Không áp dụng | Genetic optimization |
| Cotroneo et al. 2024 (#30) | Không so sánh human | Không áp dụng | System architecture study |

→ **Kết luận: XÁC NHẬN — 0/20 paper dùng sinh viên làm nhóm C**

---

### GAP-M: Không paper nào đo đồng thời branch coverage VÀ mutation score trên cùng bộ medium CC functions

| Paper | Đo branch? | Đo mutation? | Cùng bộ hàm? | Ghi chú |
|-------|-----------|-------------|-------------|---------|
| Yuan et al. 2024 (#1) | Có | Không | N/A | Chỉ branch + statement coverage |
| MDPI 2025 (#9) | Có — 97.16% | Không | N/A | Ghi rõ "Mutation score KHÔNG đo" |
| Cabral 2025 (#10) | Không riêng | Có — 85.61% | N/A | Mutation Primes (medium CC) nhưng không báo branch riêng |
| Seed&Steer 2025 (#21) | Có — 73% | Không | N/A | Không đo mutation score |
| Wang et al. 2025 (#4) | Có — 100% | Có — 4% | Không cùng CC level | **Cảnh báo quan trọng**: 2 metrics không thay thế nhau nhưng không kiểm soát CC |
| Pan et al. 2024 (#6) | Có — 63.2% | Có — một phần | Không | Không kiểm soát CC = 11–20 |
| ULT Benchmark (#8) | Có — 30.22% | Có — 40.21% | Gần nhất | Python nhưng high CC, không phải medium |
| AgoneTest 2025 (#13) | Có | Không | N/A | Không đo mutation |
| Schäfer et al. 2024 (#4 TSE) | Có | Không | N/A | Line + branch, không mutation |
| CoverUp 2025 (#14) | Có — 80% | Không | N/A | Python, không đo mutation, không kiểm soát CC |
| Các paper còn lại (#2,3,5,7,11,12,15–20) | Một số | Không | N/A | Không đo cả 2 metrics đồng thời trên cùng bộ hàm |

→ **Kết luận: XÁC NHẬN — 0/20 paper đo đồng thời cả 2 metrics trên cùng bộ medium CC functions**

---

### GAP-D: Không có benchmark Python medium CC (11–20) với mutation testing đầy đủ

| Paper | Ngôn ngữ | CC level kiểm soát? | Có mutation testing? | Ghi chú |
|-------|---------|--------------------|--------------------|---------|
| ULT Benchmark 2025 (#8) | Python | Không — high CC | Có (40.21%) | Benchmark Python duy nhất nhưng **high CC**, không phải medium |
| CoverUp 2025 (#14) | Python | Không | Không | Branch 80% nhưng không kiểm soát CC, không đo mutation |
| Cabral 2025 (#10) | Java | Có — medium CC (Primes) | Có — 85.61% | **Java**, không phải Python |
| MDPI 2025 (#9) | Java | Không | Không | Java, không đo mutation |
| Các paper còn lại | Java hoặc mixed | Không | Không | Không có Python medium CC + mutation |

→ **Kết luận: XÁC NHẬN — 0/20 paper có benchmark Python medium CC (11–20) với mutation testing đầy đủ**

---

## Feasibility Check — GAP Chính (GAP-T + GAP-M)

| Tiêu chí | Câu hỏi | Mức | Ghi chú |
|----------|---------|-----|---------|
| Dataset | Dataset Java/Python functions public có sẵn, tải được ngay? | ✅ | Defects4J (Java) + GitHub Python repos — có sẵn, lọc theo CC = 11–20 bằng radon/lizard |
| Tool/API | GPT-4 API có free tier / cost thấp cho N samples? | ⚠️ | Cần ~$5–10 API cost cho ~100 functions × 2 ngôn ngữ; < $10 tổng |
| Compute | CPU đủ chạy MutPy + JUnit/pytest? | ✅ | CPU hoặc Colab T4 free đủ; mutation testing tốn thời gian nhưng không cần GPU |
| Ground truth | Cần annotation thủ công không? | ⚠️ | Cần sinh viên viết test thủ công — ước tính 2–3 buổi lab (~6 giờ) cho nhóm 5–10 sinh viên |
| Skills | Có thư viện MutPy, Coverage.py, JaCoCo? | ✅ | pip install mutpy, coverage; JaCoCo là Maven plugin — có tutorial đầy đủ |
| Thời gian | Experiment hoàn thành trong deadline? | ✅ | Xong với buffer ≥ 1 tuần; mutation testing tự động sau khi set up pipeline |
| Contribution | Kết quả âm tính có giá trị? | ✅ | Là nghiên cứu đầu tiên so GPT-4 với sinh viên + đo đồng thời 2 metrics trên medium CC |

**Kết quả: 0 ❌ / 2 ⚠️ → An toàn — tiếp tục với GAP này**
