# Research Proposal: LLM for Unit Test Case Generation

---

## 1. Tiêu Đề & Thông Tin Nhóm

**Tên đề tài:** Evaluating GPT-4o mini Zero-Shot for Unit Test Generation on Python Functions

**Nhóm:** Nhóm 5

**Thành viên:**

| Họ và tên            | Vai trò |
| -------------------- | ------- |
| Lê Quang Thắng       | Leader  |
| Đặng Nguyễn Quốc Huy | Member  |
| Nguyễn Hữu Khánh Duy | Member  |
| Nguyễn Hoàng Hùng    | Member  |
| Trịnh Duy Khang      | Member  |

**Topic code:** [RT-SWT-004]

**Ngày nộp:** 2026-06-19

**Version:** 1.1

**Trạng thái:** Đang chờ phê duyệt

---

## 2. Research Problem Statement

### 2.1 Bối cảnh & Tầm quan trọng

Unit testing là hoạt động kiểm thử phần mềm cốt lõi nhằm phát hiện lỗi sớm và đảm bảo độ tin cậy của phần mềm. Tuy nhiên, việc viết test thủ công tốn nhiều thời gian và thường bị bỏ qua trong thực tế phát triển. Gần đây, các mô hình ngôn ngữ lớn (LLM) đã cho thấy tiềm năng trong việc tự động sinh test case — theo Wang et al. (HITS, ASE 2024), HITS đạt branch coverage trung bình 48.12% trên các Java method phức tạp, vượt EvoSuite (38.46%). Tuy nhiên, hầu hết nghiên cứu tập trung vào GPT-3.5/GPT-4 với các framework phức tạp, trong khi khả năng của các mô hình chi phí thấp hơn như GPT-4o mini trong điều kiện zero-shot vẫn chưa được đánh giá độc lập.

### 2.2 State of the Art

Các nghiên cứu hiện tại đã khám phá nhiều hướng tiếp cận khác nhau cho bài toán sinh unit test tự động:

- **Wang et al. (HITS, ASE 2024)** dùng GPT-3.5-turbo với method slicing và CoT trên 114 Java method (CC > 10), đạt branch coverage 48.12% — vượt EvoSuite 38.46%.
- **Tang et al. (IEEE TSE 2024)** so sánh ChatGPT zero-shot với EvoSuite trên 207 Java class; EvoSuite áp đảo (statement coverage 74.2% vs 55.4%), nhưng ChatGPT tạo test dễ đọc hơn.
- **Guerino & Vincenzi (SBQS 2025)** đánh giá ChatGPT-3.5 trên 40 Python program nhỏ với feedback loop, đạt decision coverage 95.9% và mutation score 91.5%, vượt Pynguin.
- **Aminata et al. (2SZSP, WSSE 2025)** dùng Mistral 7B zero-shot hai bước trên 4 Java project; đáng chú ý, 2SZSP **thắng EvoSuite về mutation score** (41.3% vs 30.8%) dù thua về coverage.
- **Huang et al. (ULT Bench, TOSEM 2026)** benchmark 12 LLM trên Python dataset chống data leakage; branch coverage trung bình chỉ đạt 30.22% — chứng minh năng lực LLM bị thổi phồng do data contamination.

### 2.3 GAP

**GAP-T (Primary):** Không có nghiên cứu nào trong 8 paper đánh giá GPT-4o mini (zero-shot thuần, không framework bổ sung) trực tiếp trên Python functions có Cyclomatic Complexity 5–15, đồng thời đo cả branch coverage và mutation score, và so sánh với Pynguin. Các nghiên cứu dùng GPT-3.5/GPT-4 đều kết hợp method slicing (HITS), AST traversal (SymPrompt), hoặc CoT multi-step (Ouédraogo et al.), hoặc không báo cáo mutation score (Tang et al., Paper 3, Paper 4), hoặc chỉ so với EvoSuite — không so với Pynguin trên dải CC 5–15.

**GAP-D (Secondary):** Không có dataset nào cô lập chính xác dải CC 5–15 cho Python trong một benchmark duy nhất. ULT Bench dùng CC ≥ 10 (Python), SymPrompt không filter CC.

**GAP-M (Secondary):** Chỉ 3/8 paper báo cáo mutation score; không paper nào kết hợp branch coverage và mutation score như ngưỡng pass/fail kép trên Python functions với CC 5–15.

### 2.4 Motivation

Nếu không giải quyết GAP này, các nhóm phát triển và tổ chức giáo dục không có cơ sở thực nghiệm để đánh giá liệu GPT-4o mini — mô hình có chi phí thấp hơn GPT-4 ~15 lần — có đủ hiệu quả để dùng trong quy trình kiểm thử thực tế hay không. Điều này đặc biệt quan trọng với các nhóm nhỏ và sinh viên không có ngân sách lớn cho API.

---

## 3. Related Work

### 3.1 Overview

| Paper                                           | Tool/LLM                                  | Dataset                                | Metric                           | Best Result                            | Hạn chế chính                         |
| ----------------------------------------------- | ----------------------------------------- | -------------------------------------- | -------------------------------- | -------------------------------------- | ------------------------------------- |
| HITS (Wang et al., ASE 2024)                    | GPT-3.5 + Method Slicing + CoT            | 114 Java methods (CC > 10)             | Branch Cov                       | 48.12%                                 | Java only; không có mutation score    |
| ChatGPT vs SBST (Tang et al., TSE 2024)         | ChatGPT GPT-3 zero-shot                   | 207 Java classes                       | Statement Cov                    | 55.4% (vs EvoSuite 74.2%)              | Java only; không có mutation score    |
| LLMs and Prompting (Ouédraogo et al., ASE 2024) | GPT-3.5/4, Mistral, Mixtral; 5 strategies | SF110, Defects4J, CMD                  | Line/Method Cov                  | GToT tốt nhất trên CMD                 | Java only; không có mutation score    |
| SymPrompt (Ryan et al., FSE 2024)               | CodeGen2 16B + GPT-4 + AST traversal      | 897 Python focal methods               | Branch Cov                       | 44% (filtered: 66%)                    | Python only; không có mutation score  |
| ChatGPT Python (Guerino & Vincenzi, SBQS 2025)  | ChatGPT-3.5 + feedback loop               | 40 Python programs (32.2 SLOC avg)     | Decision Cov, Mutation Score     | 95.9% cov; 91.5% mut                   | Python only; code quá nhỏ và đơn giản |
| 2SZSP (Aminata et al., WSSE 2025)               | Mistral 7B zero-shot 2-step               | 4 Java projects (70 classes)           | Branch Cov, Mutation Score       | Mutation: 41.3% (thắng EvoSuite 30.8%) | 64% test không compile được           |
| GPT-4o vs DeepSeek (Cabral et al., SBQS 2025)   | GPT-4o + DeepSeek Chat V3 + PIT           | 6 Java classes từ Defects4J (CC 17–77) | Compilation Rate, Mutation Score | GPT-4o CSR: 63.33%                     | Dataset quá nhỏ; thủ công hoàn toàn   |
| ULT Bench (Huang et al., TOSEM 2026)            | 12 SOTA LLMs; K-query iterative           | 3,909 Python functions (CC ≥ 10)       | BCov@k, Mut@k                    | BCov@5: 30.22%                         | Python only; không có GPT-4o mini     |

### 3.2 Pattern Analysis

Nhìn chung, các nghiên cứu hiện tại cho thấy ba xu hướng rõ ràng: (1) LLM với framework bổ sung (method slicing, AST traversal, feedback loop) vượt trội LLM zero-shot đơn thuần — thể hiện qua HITS (48.12%) và SymPrompt (66% filtered) so với ChatGPT zero-shot (44%); (2) hầu hết nghiên cứu chỉ đánh giá một ngôn ngữ và không đo mutation score — thể hiện qua 5/8 paper chỉ có Java hoặc Python, và chỉ 3/8 paper báo cáo mutation score; (3) ULT Bench (Huang et al., 2026) chứng minh data contamination thổi phồng kết quả đáng kể, với BCov@5 giảm từ ~44% (PLT leaked) xuống 30.22% (ULT unleaked).

### 3.3 GAP Mapping

| GAP                                                                    | Loại  | Paper support (N = 8)                                                  | Status    |
| ---------------------------------------------------------------------- | ----- | ---------------------------------------------------------------------- | --------- |
| GPT-4o mini zero-shot chưa đánh giá độc lập trên CC 5–15               | GAP-T | 8/8 paper không dùng GPT-4o mini zero-shot                             | Confirmed |
| Không có dataset cô lập CC 5–15 cả Java lẫn Python                     | GAP-D | 3/8 paper có filter CC (HITS CC>10, ULT CC≥10, SymPrompt không filter) | Confirmed |
| Không paper nào kết hợp branch cov + mutation score như ngưỡng kép     | GAP-M | 3/8 báo cáo mutation score; 0/8 dùng ngưỡng kép                        | Confirmed |
| Không paper nào so Pynguin trên Python CC 5–15; hầu hết chỉ 1 ngôn ngữ | GAP-S | 5/8 paper chỉ 1 ngôn ngữ; 0/8 so với Pynguin trên dải CC 5–15          | Confirmed |

---

## 4. Research Questions

> **Chốt tại đây. Sau khi GV phê duyệt, không được thay đổi RQ, metric, hay threshold.**

### RQ1: GPT-4o mini Zero-Shot — Absolute Quality Threshold

**RQ1:** [P: Python functions có CC = 5–15] + [I: GPT-4o mini zero-shot, temperature = 0] có đạt [O: Branch Coverage ≥ 50% VÀ Mutation Score ≥ 40% VÀ Compilation Success Rate ≥ 80%] không?

**Loại claim:** Absolute threshold

**H0₁:** GPT-4o mini zero-shot KHÔNG đạt Branch Coverage ≥ 50% AND Mutation Score ≥ 40% AND Compilation Success Rate ≥ 80% trên Python functions có CC = 5–15.

**H1₁:** GPT-4o mini zero-shot ĐẠT Branch Coverage ≥ 50% AND Mutation Score ≥ 40% AND Compilation Success Rate ≥ 80% trên Python functions có CC = 5–15.

**Metric:** Branch Coverage (coverage.py); Mutation Score (Cosmic-Ray); Compilation Success Rate
**Ngưỡng:** Branch Coverage ≥ 50% (floor từ literature: HITS 48.12%, SymPrompt 44%, ULT 30.22%, 2SZSP 31.3%); Mutation Score ≥ 40% (floor từ literature: HITS 36.25%, ULT 33.59%, 2SZSP 30.8%); CSR ≥ 80% (threshold thực tiễn tối thiểu cho pipeline tự động)
**Statistical test:** Wilcoxon signed-rank (α = 0.05) cho branch coverage và mutation score (liên tục, paired); Binomial exact test (α = 0.05) cho Compilation Success Rate (nhị phân). Áp dụng Bonferroni correction do 3 metric: α_adjusted = 0.05/3 = 0.0167.

---

### RQ2: GPT-4o mini Zero-Shot vs. Pynguin

**RQ2:** [P: Python functions có CC = 5–15] + [I: GPT-4o mini zero-shot, temperature = 0] có tốt hơn [C: Pynguin] về [O: Branch Coverage và Mutation Score] không?

**Loại claim:** Comparative

**H0₂:** GPT-4o mini zero-shot KHÔNG tốt hơn Pynguin về Branch Coverage và Mutation Score trên Python functions có CC = 5–15.

**H1₂:** GPT-4o mini zero-shot TỐT HƠN Pynguin về Branch Coverage và Mutation Score trên Python functions có CC = 5–15.

**Metric:** Branch Coverage (coverage.py); Mutation Score (Cosmic-Ray)
**Ngưỡng:** TBD — derive từ pilot run Pynguin trên 5–10 sample functions (Case 2: floor value). Amendment sẽ được ghi sau pilot Tuần 7.
**Statistical test:** Wilcoxon signed-rank, one-tailed (α = 0.05) — paired per function vì GPT-4o mini và Pynguin chạy trên cùng tập functions. Effect size: Cliff's delta.

---

## 5. Experiment Protocol

### 5.1 Pipeline Tổng Quan

Pipeline gồm 5 bước thực hiện tuần tự, đủ chi tiết để người khác chạy lại:

1. **Thu thập & lọc dataset:** Download CodeXGLUE hoặc crawl GitHub → tính CC bằng Radon (Python) → giữ CC = 5–15 → loại getter/setter (< 5 SLOC) → lấy ngẫu nhiên theo stratified sampling.
2. **Chuẩn bị baseline:** Chạy Pynguin (algorithm DYNAMOSA, seed = 42, time-limit = 60s) trên từng function → lưu automated test suite làm baseline cho RQ2.
3. **Chạy LLM:** Gửi từng function qua GPT-4o mini API (batch) theo prompt template zero-shot → lưu output JSON → log API cost.
4. **Đo metric:** Chạy coverage.py (Python) → Cosmic-Ray (Python) → ghi kết quả vào CSV.
5. **Phân tích thống kê:** Wilcoxon signed-rank + Binomial exact test → tính effect size (Cliff's delta) → so sánh với Pynguin baseline.

### 5.2 Dataset

| Thuộc tính        | Chi tiết                                                                                                                                          |
| ----------------- | ------------------------------------------------------------------------------------------------------------------------------------------------- |
| Tên dataset       | CodeXGLUE (Microsoft) — lọc lại theo CC                                                                                                           |
| Nguồn             | github.com/microsoft/CodeXGLUE — Python split                                                                                                     |
| URL mẫu           | https://github.com/microsoft/CodeXGLUE                                                                                                            |
| Quy mô (N)        | Mục tiêu: 50 Python functions; tối thiểu: 30 functions                                                                                            |
| Domain            | Cấu trúc dữ liệu, thuật toán, utility functions                                                                                                   |
| Preprocessing     | Tính CC bằng Radon (Python); giữ CC = 5–15; loại bỏ function < 5 SLOC (getter/setter); loại bỏ function có external dependency không resolve được |
| Sampling strategy | Stratified theo CC band: CC 5–8 (40%), CC 9–12 (40%), CC 13–15 (20%)                                                                              |
| Lý do chọn        | GAP-D — không benchmark sẵn có cô lập đúng dải CC 5–15 cho Python; dùng CodeXGLUE để tránh data contamination (xem ULT Bench, Huang et al. 2026)  |
| Verify status     | ⚠️ TBD — sẽ verify accessible và download thử trước khi nộp proposal                                                                              |

### 5.3 LLM/Tool Configuration

**Model:** `gpt-4o-mini` (version: `gpt-4o-mini-2024-07-18` — pin version để reproducibility)
**Hyperparameters:** temperature = 0, top_p = 1, max_tokens = 2048, frequency_penalty = 0
**Prompting strategy:** Zero-shot (không CoT, không few-shot, không method slicing)
**Prompt template (nguyên văn):**

```
You are a senior software engineer. Generate a complete pytest test module for the following Python function. The test module must:
- Cover all branches of the function
- Use descriptive test function names
- Not require external dependencies beyond pytest
- Run without modification

Function under test:
{function_source_code}

Generate only the test module code, no explanations.
```

**Lý do chọn GPT-4o mini:** Chi phí thấp hơn GPT-4o ~15 lần (0.15 USD/1M input tokens vs 2.50 USD/1M), cho phép chạy large-scale experiment trong ngân sách capstone. Đây là điểm phân biệt với các paper đã dùng GPT-3.5-turbo (HITS) hoặc GPT-4o (Cabral et al.).

**Lý do chọn temperature = 0:** Reproducibility — output xác định, không phụ thuộc vào random seed. Khác với Guerino & Vincenzi (2025) thử 11 mức temperature; nghiên cứu này cố định để đo baseline rõ ràng.

### 5.4 Measurement

| Metric                   | Tool + version               | Ground truth source                      | Ghi chú                              |
| ------------------------ | ---------------------------- | ---------------------------------------- | ------------------------------------ |
| Branch Coverage (Python) | coverage.py 7.x + pytest 8.x | Generated test suite vs. function source | `--branch` flag                      |
| Mutation Score (Python)  | Cosmic-Ray 9.x               | Generated test suite                     | Standard operators                   |
| Compilation Success Rate | Python interpreter           | N/A                                      | Binary: compile thành công hay không |

### 5.5 Baseline

**Baseline cho RQ2:** Pynguin v3.8 (Python)
**Cấu hình Pynguin:** algorithm = DYNAMOSA, seed = 42, time-limit = 60s, criterion = branch coverage
**Cấu hình reproduce:** `pynguin --project-path ./functions --module-name {module} --output-path ./baseline --algorithm DYNAMOSA --seed 42 --maximum-search-time 60`
**Lý do chọn Pynguin:** GAP-S — Pynguin là tool tương đương EvoSuite dành riêng cho Python; không paper nào trong N = 8 so sánh GPT-4o mini với Pynguin trên dải CC 5–15.

### 5.6 Statistical Analysis Plan

**RQ1 — Wilcoxon signed-rank test (one-tailed, α_adjusted = 0.0167 sau Bonferroni correction cho 3 metric):**

- Input: Branch coverage scores của GPT-4o mini trên 50 Python functions
- H0 reject khi: p < 0.0167 AND median branch coverage GPT-4o mini ≥ 50%
- Effect size: Cliff's delta (ngưỡng: small |d| ≥ 0.147, medium ≥ 0.33, large ≥ 0.474)
- N và power: N ≥ 60 functions → power ≥ 0.80 theo G\*Power (Wilcoxon, effect size medium, α = 0.05)

**RQ1 — Wilcoxon signed-rank test (one-tailed, α_adjusted = 0.0167) cho Mutation Score:**

- Input: Mutation score của GPT-4o mini trên 50 Python functions
- H0 reject khi: p < 0.0167 AND median mutation score GPT-4o mini ≥ 40%
- Effect size: Cliff's delta

**RQ1 — Binomial exact test (one-tailed, α_adjusted = 0.0167) cho Compilation Success Rate:**

- H0 reject khi: p < 0.0167 AND observed CSR ≥ 80%
- Effect size: Cohen's h

**RQ2 — Wilcoxon signed-rank test (one-tailed, α = 0.05) — paired per function:**

- Input: Branch coverage và mutation score của GPT-4o mini vs. Pynguin (cùng tập functions)
- H0 reject khi: p < 0.05 AND GPT-4o mini > Pynguin
- Threshold cụ thể: TBD từ pilot (Amendment Tuần 7)
- Effect size: Cliff's delta

---

## 6. Evaluation Plan

### 6.1 Bảng Tiêu Chí Đánh Giá

| RQ  | Metric                   | Ngưỡng                   | Test                                  | H0 bị reject khi...                | Kết quả âm tính có ý nghĩa?                                                     |
| --- | ------------------------ | ------------------------ | ------------------------------------- | ---------------------------------- | ------------------------------------------------------------------------------- |
| RQ1 | Branch Coverage          | ≥ 50%                    | Wilcoxon signed-rank (α_adj = 0.0167) | p < 0.0167 AND median ≥ 50%        | Có — xác nhận GPT-4o mini không đủ cho production; cần framework bổ sung        |
| RQ1 | Mutation Score           | ≥ 40%                    | Wilcoxon signed-rank (α_adj = 0.0167) | p < 0.0167 AND median ≥ 40%        | Có — cho thấy test sinh ra ít phát hiện lỗi; gap so với paper có mutation > 40% |
| RQ1 | Compilation Success Rate | ≥ 80%                    | Binomial exact test (α_adj = 0.0167)  | p < 0.0167 AND observed CSR ≥ 80%  | Có — nếu CSR thấp, pipeline không dùng được thực tế                             |
| RQ2 | Branch Coverage          | ≥ Pynguin (TBD từ pilot) | Wilcoxon signed-rank (α = 0.05)       | p < 0.05 AND GPT-4o mini > Pynguin | Có — nếu LLM không thắng Pynguin, không có lý do dùng LLM cho CC 5–15           |
| RQ2 | Mutation Score           | ≥ Pynguin (TBD từ pilot) | Wilcoxon signed-rank (α = 0.05)       | p < 0.05 AND GPT-4o mini > Pynguin | Có — tương tự như trên                                                          |

### 6.2 Diễn Giải Tổ Hợp Kết Quả

| Tình huống                                       | Kết luận                                                                             |
| ------------------------------------------------ | ------------------------------------------------------------------------------------ |
| RQ1: Branch Cov ✓ AND Mutation Score ✓ AND CSR ✓ | Double positive — GPT-4o mini zero-shot đủ dùng cho CC 5–15                          |
| RQ1: Branch Cov ✓ nhưng Mutation Score ✗         | Mixed — coverage tốt nhưng test yếu về fault detection; cần mutation-aware prompting |
| RQ1: tất cả ✗                                    | Double negative — GPT-4o mini zero-shot không đủ; cần framework (CoT, slicing)       |
| RQ2: GPT-4o mini > Pynguin                       | LLM có giá trị gia tăng so với random baseline                                       |
| RQ2: GPT-4o mini ≤ Randoop                       | Null result — đáng công bố vì không paper nào đo so sánh này                         |

### 6.3 Sub-group Analysis (nếu có)

Điều kiện: n_group ≥ 15 per CC band để chạy sub-group. Quyết định TRƯỚC khi có data:

- So sánh kết quả theo CC band: CC 5–8 vs. CC 9–12 vs. CC 13–15

---

## 7. Threats to Validity

### 7.1 Internal Validity

**Threat 1:** Model version drift — OpenAI có thể silent-update `gpt-4o-mini` giữa các lần chạy, gây kết quả không nhất quán.
**Mitigation:** Pin version = `gpt-4o-mini-2024-07-18` trong tất cả API call; log version string thực tế trả về từ API response header; chạy toàn bộ experiment trong 1 tuần liên tục (Tuần 8).

**Threat 2:** Data contamination — CodeXGLUE có thể đã xuất hiện trong training data của GPT-4o mini, thổi phồng kết quả.
**Mitigation:** Ghi rõ limitation này trong §8.1; so sánh với ULT Bench (Huang et al. 2026) làm reference point; ưu tiên các functions ít phổ biến trong dataset.

### 7.2 External Validity

**Threat 1:** Dataset GitHub không đại diện cho codebase thực tế — GitHub thiên về open-source projects, có thể có style code khác corporate code.
**Mitigation:** Lọc theo nhiều domain (data structures, algorithms, utility); ghi rõ trong §8.1 rằng kết quả áp dụng cho "open-source functions CC 5–15" không generalize sang industrial code.

**Threat 2:** CC 5–15 là dải hẹp, không đại diện cho toàn bộ phổ complexity.
**Mitigation:** Ghi rõ scope giới hạn trong abstract; sub-group analysis theo CC band nếu đủ N.

### 7.3 Construct Validity

**Threat 1:** Branch coverage không đo semantic correctness — test có thể đạt coverage cao nhưng assertion sai hoặc tầm thường (e.g., `assertTrue(true)`).
**Mitigation:** Kết hợp mutation score như metric phụ; mutation score phản ánh khả năng detect fault thực sự, không chỉ cover code.

**Threat 2:** Threshold tuyệt đối (BC ≥ 50%, MS ≥ 40%, CSR ≥ 80%) được đặt dựa trên literature — nếu threshold không phù hợp với đặc điểm dataset thực tế, kết luận RQ1 có thể bị ảnh hưởng.
**Mitigation:** Justify từng threshold từ floor value của ≥ 4 paper trong SLR; báo cáo kết quả thực tế song song với kết luận threshold để reader tự đánh giá.

### 7.4 Conclusion Validity

**Threat 1:** N nhỏ (60–100 functions) có thể thiếu statistical power cho sub-group analysis.
**Mitigation:** Power analysis trước: N ≥ 60 đảm bảo power ≥ 0.80 cho overall test; sub-group chỉ chạy nếu n_group ≥ 15; báo cáo confidence interval bên cạnh p-value.

**Threat 2:** Multiple testing — chạy nhiều test (RQ1 × 3 metric, RQ2 × 2 metric) làm tăng Type I error.
**Mitigation:** Áp dụng Bonferroni correction cho RQ1 (α_adjusted = 0.0167, xem §5.6); RQ2 dùng α = 0.05 (2 metric không phải family của RQ1). Báo cáo p-value gốc song song với adjusted để reader tự đánh giá.

---

## 8. Timeline & Resources

### 8.0 Phân Công Vai Trò

| Role | Thành viên           | Trách nhiệm trong experiment                                                           |
| ---- | -------------------- | -------------------------------------------------------------------------------------- |
| PL   | Nguyễn Hoàng Hùng    | Điều phối tiến độ, review nhật ký toàn proposal, submit GV, xử lý blockers             |
| DG   | Nguyễn Hữu Khánh Duy | Thu thập + clean dataset (CodeXGLUE), lọc CC bằng Radon, chạy Pynguin baseline         |
| LR   | Đặng Nguyễn Quốc Huy | Cấu hình API, viết script chạy experiment, batch processing toàn bộ input, log chi phí |
| MS   | Lê Quang Thắng       | Implement metrics (coverage.py, Cosmic-Ray), chạy statistical tests, tính effect size  |
| RW   | Trịnh Duy Khang      | Viết §1, §7, intro, conclusion; hỗ trợ DG viết §3; tạo figures; format document cuối   |

> **Quy tắc bất biến:** LR và MS không được gộp vào 1 người — người chạy experiment không được tự verify kết quả của chính mình.

### 8.1 Resource Inventory

| Tài nguyên                       | Trạng thái | Owner | Ghi chú                                                           |
| -------------------------------- | ---------- | ----- | ----------------------------------------------------------------- |
| Dataset (CodeXGLUE Python split) | ⚠️ TBD     | DG    | Download từ github.com/microsoft/CodeXGLUE; cần verify CC filter  |
| API key (OpenAI GPT-4o mini)     | ✅/⚠️      | LR    | Free tier giới hạn; ước tính chi phí trước khi chạy full          |
| Compute                          | ✅/⚠️      | LR    | Colab T4 / Kaggle P100 / local CPU; mutation testing cần Colab T4 |
| coverage.py + pytest             | ✅         | MS    | Free, pip install                                                 |
| Cosmic-Ray                       | ✅         | MS    | Free, pip install                                                 |
| Radon                            | ✅         | DG    | Free, pip install — tính CC cho Python                            |
| Pynguin v3.8                     | ✅         | DG    | Free, pip install — automated baseline cho RQ2                    |

### 8.2 Chi Phí Ước Tính

| Item                      | Số lượng                     | Đơn giá              | Tổng           | Ghi chú                                 |
| ------------------------- | ---------------------------- | -------------------- | -------------- | --------------------------------------- |
| GPT-4o mini input tokens  | ~50 functions × ~500 tokens  | 0.15 USD / 1M tokens | ~0.004 USD     | Ước tính; thực tế log từ API            |
| GPT-4o mini output tokens | ~50 functions × ~1000 tokens | 0.60 USD / 1M tokens | ~0.03 USD      |                                         |
| Tổng API cost (ước tính)  | —                            | —                    | **< 0.05 USD** | Rất thấp; free tier OpenAI đủ cho pilot |
| Compute (Colab T4)        | ~10 giờ mutation testing     | Free                 | 0 USD          | Colab free tier đủ nếu chạy batch nhỏ   |

### 8.3 Timeline Chi Tiết (Tuần 5–10)

> Tuần 5–6: Song song viết proposal + chuẩn bị tài nguyên
> Tuần 7–8: Thực nghiệm (Pilot → Full)
> Tuần 9–10: Viết paper + present

| Tuần     | Hoạt động                                                | Owner        | Checkpoint — output cụ thể                                  |
| -------- | -------------------------------------------------------- | ------------ | ----------------------------------------------------------- |
| **5\***  | Viết proposal §2–§7 (RBL-2.1 → RBL-3.1 Bước 3)           | DG + RW + PL | Draft §2–§7 trong `data/raw/` folder + README mô tả dataset |
| **5\***  | Verify + clean dataset, kiểm tra format                  | DG           | `data/raw/` folder + README                                 |
| **5\***  | Setup API, test 1 sample call, xác nhận budget           | LR           | `test_api.py` chạy được + output 1 test suite               |
| **5\***  | Implement metric script sơ bộ, test data giả             | MS           | `compute_metric.py` draft — chạy được trên mock data        |
| **5\***  | Hoàn thiện §8 + resource inventory + nộp GV              | PL           | `proposal.md` v1.0 — nộp GV                                 |
| **6\***  | ★ **GV phê duyệt proposal** (hard deadline: cuối Tuần 6) | GV           | `proposal.md` → Trạng thái: Approved                        |
| **7\***  | Chuẩn bị pilot dataset + chạy Pynguin baseline           | DG           | `data/pilot_functions.csv` + `baseline/pilot_pynguin/`      |
| **7\***  | Chạy LLM trên pilot sample                               | LR           | `results/pilot_llm_output.csv` + API log                    |
| **7\***  | Tính metric pilot, kiểm tra phân phối                    | MS           | `results/pilot_analysis.ipynb` — histogram + phân phối      |
| **7\***  | **All: Họp review pilot → amendment nếu cần**            | PL           | Meeting note. Amendment → nộp GV trong 24 giờ               |
| **8\***  | Chuẩn bị full dataset + chạy Pynguin baseline đầy đủ     | DG           | `data/full_functions.csv` + `baseline/full_pynguin/`        |
| **8\***  | Full experiment batch run                                | LR           | `results/full_llm_output.csv` + cost log                    |
| **8\***  | Tính metric toàn bộ + statistical tests                  | MS           | `results/full_analysis.ipynb` — p-value + effect size       |
| **8\***  | Tạo figures (≥ 2 plots)                                  | RW           | `figures/` — boxplot + distribution                         |
| **9–10** | Viết paper + present                                     | Tất cả       | Xem RBL-5                                                   |

### 8.4 Contingency Plan

**Nếu proposal chưa duyệt cuối Tuần 6:** Chỉ làm RQ1, bỏ RQ2 — báo GV ngay.
**Nếu API rate limit:** Chia batch, chạy qua đêm, hoặc dùng model nhỏ hơn (cần amendment).
**Nếu dataset inaccessible:** Dùng dataset thay thế: BugsInPy (Python — https://github.com/soarsmu/BugsInPy) hoặc crawl GitHub trực tiếp; lọc lại theo CC 5–15 bằng Radon. Cần amendment ghi rõ tên dataset thay thế và kết quả verify.
**Nếu ground truth pilot Tuần 7 phát hiện vấn đề kỹ thuật:** Amendment nêu vấn đề cụ thể, nộp GV trong 24 giờ.
**Nếu thành viên không kịp deadline:** PL escalate sau 48 giờ trễ; redistribute task.

### 8.5 Checkpoint Per Member (Tuần 5–10)

| Role   | Tuần 5                    | Tuần 6                              | Tuần 7                                     | Tuần 8                                  | Tuần 9–10             |
| ------ | ------------------------- | ----------------------------------- | ------------------------------------------ | --------------------------------------- | --------------------- |
| **PL** | Draft §2–§7 review        | Submit proposal + theo dõi GV duyệt | Pilot meeting note                         | Verify §4↔§6 nhất quán                  | Final review + submit |
| **DG** | `data/raw/` + README      | Confirm §8.1 resource               | `data/pilot_functions.csv` + Pynguin run   | `data/full_functions.csv` + Pynguin run | Verify §3 data        |
| **LR** | `test_api.py` pass        | Confirm API budget                  | `results/pilot_llm_output.csv` + log       | `results/full_llm_output.csv` + cost    | —                     |
| **MS** | `compute_metric.py` draft | Confirm stat test plan              | `results/pilot_analysis.ipynb` + phân phối | `results/full_analysis.ipynb` + p-value | —                     |
| **RW** | Draft §7 Threats          | Format + proofread §1–§7            | —                                          | `figures/` folder                       | Draft §1 + conclusion |

### 8.6 Quy Trình Amendment (Khi Pilot Tuần 7 Phát Hiện Vấn Đề Kỹ Thuật)

**Khi nào cần amendment — khi nào không:**

| Phát hiện từ pilot                                            | Cần amendment?                          | Lý do                                      |
| ------------------------------------------------------------- | --------------------------------------- | ------------------------------------------ |
| Phân phối data khác loại dự kiến (bimodal, heavy-tail)        | ✅ Đổi statistical test                 | Lý do kỹ thuật                             |
| Metric không tính được do lỗi implementation hoặc data format | ✅ Đổi implementation hoặc tool version | Lý do kỹ thuật                             |
| N thực tế nhỏ hơn N trong proposal (dataset thiếu rows)       | ✅ Cập nhật §5.2 + power analysis       | Lý do kỹ thuật                             |
| Kết quả pilot thấp hơn threshold                              | ❌ Không amendment                      | Đây là kết quả — không phải lý do thay đổi |
| Muốn thêm metric vì thấy kết quả thú vị                       | ❌ Không amendment                      | HARKing — vi phạm khoa học                 |

**Thời hạn:** Nộp amendment trong 24 giờ sau pilot meeting. Nếu GV chưa phản hồi sau 48 giờ → PL escalate.

**Template Amendment** (điền vào `proposal-amendment-v1.1.md`):

```markdown
# Proposal Amendment [v1.0 → v1.1] – [Topic]

**Nhóm:** | **Ngày:** | **Lý do:** Phát hiện từ pilot Tuần 7

## Vấn đề phát hiện

[Mô tả vấn đề kỹ thuật cụ thể]

## Thay đổi đề xuất

| Mục       | Proposal v1.0 | Đề xuất v1.1   | Lý do kỹ thuật    |
| --------- | ------------- | -------------- | ----------------- |
| §5.6 Test | Wilcoxon      | Mann-Whitney U | Phân phối bimodal |

## Sections bị ảnh hưởng

- [ ] §4: H0/H1 cập nhật
- [ ] §5.6: Statistical test plan cập nhật
- [ ] §6.1: Reject condition cập nhật

**Đính kèm:** `results/pilot_analysis.ipynb` (bằng chứng kỹ thuật)
**Xin phê duyệt GV:** [ ] Approved – Ngày: \_\_\_\_
```

---

_End of proposal v1.1 — Đang chờ phê duyệt GV_
