# Experiment Design Rationale – LLM for Unit Test Case Generation

Ngày: 2026-06-11 | GAP source: SLR/gap-analysis.md

---

## Bảng Quyết Định

| Quyết định       | Giá trị                                                                                             | Nguồn gốc                                                                                                                                                                                |
| ---------------- | --------------------------------------------------------------------------------------------------- | ---------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------- |
| LLM/Tool         | GPT-4o mini (version: gpt-4o-mini)                                                                 | GAP-T — cột Tool/LLM trong evidence table; không paper nào đánh giá GPT-4o mini zero-shot thuần                                                                                                |
| Dataset chính    | Java/Python functions từ GitHub open-source, CC = 5–15, đã lọc bằng Lizard (Java) và Radon (Python) | GAP-D — không benchmark sẵn có cô lập dải CC này                                                                                                                                         |
| Metric chính     | Branch Coverage (%)                                                                                 | GAP-M — metric phổ biến nhất: ≥ ceil(0.4×8) = 4 paper dùng (Paper 1, 2, 3, 4)                                                                                                            |
| Metric phụ       | Mutation Score (%) đo bằng PIT (Java) và Cosmic-Ray (Python)                                        | GAP-M — chỉ 3/8 paper đo mutation score; đây là gap metric chính                                                                                                                         |
| Threshold RQ1    | Branch Cov: 50%; Mutation Score: 40%                                                                | Case 1 – floor từ literature LLM: Branch Cov (HITS 48.12%, SymPrompt 44%, ULT 30.22%, 2SZSP 31.3%) → ceiling 50%; Mutation Score (HITS 36.25%, ULT 33.59%, 2SZSP 30.8%) → ceiling 40%. Chi tiết tại mục "Lý giải threshold" bên dưới. |
| Threshold RQ2    | Tương đương hoặc cao hơn Randoop                                                                    | Case 1 – không paper nào đo Randoop; dùng floor = output Randoop thực tế khi pilot                                                                                                       |
| Pipeline base    | Evaluation paradigm từ Paper 2 (Tang et al., TSE 2024) và Paper 5 (Guerino & Vincenzi, SBQS 2025)   | Gần nhất với setting zero-shot + feedback loop                                                                                                                                           |
| Statistical Test | Wilcoxon signed-rank (branch cov liên tục) + Binomial exact test (pass rate executable)             | Bước 5B — output liên tục và nhị phân                                                                                                                                                    |

---


## Lý do chọn GPT-4o mini

GPT-4o mini was selected because it offers a significantly lower inference cost while maintaining strong code-generation capabilities, making large-scale experimentation feasible within project constraints. This positions the study as evaluating **cost-effective LLM-based unit test generation** — a practical framing suitable for capstone/thesis scope and directly relevant to real-world adoption of affordable LLMs for software testing tasks.

---

## Lý giải threshold (1 đoạn cho mỗi threshold)

**Threshold RQ1 – Branch Coverage ≥ 50%:**

Derived from literature:

- HITS: 48.12%
- SymPrompt: 44%
- ULT: 30.22%
- 2SZSP: 31.3%

Threshold 50% được chọn vì cao hơn mức trung bình của phần lớn nghiên cứu hiện có nhưng vẫn nằm trong phạm vi khả thi đối với GPT-4o mini.

**Threshold RQ1 – Mutation Score ≥ 40%:**
Mutation Score threshold = 40%

Derived from literature:

- HITS: 36.25%
- ULT: 33.59%
- 2SZSP: 30.8%

Threshold 40% được chọn vì nó vượt qua mức trung bình từ các nghiên cứu hiện tại và cao hơn so với Random (thường < 30%), đồng thời thể hiện rõ hơn khả năng phát hiện lỗi của LLM.

**Threshold RQ2 – So với Randoop:**
Case 2 (floor value từ pilot) — không paper nào trong N = 8 đo Randoop, nên không có Case 1. Threshold sẽ được xác định sau khi chạy Randoop trên 5–10 sample functions trong pilot (PRE-PROPOSAL). Ghi rõ trong hypotheses-draft.md là "threshold TBD – từ pilot run Randoop".

---

## Pipeline (3 thành phần chính)

| Thành phần      | Ghi rõ                                                                                                                | Nguồn |
| --------------- | --------------------------------------------------------------------------------------------------------------------- | ----- |
| LLM/Tool        | GPT-4o mini (gpt-4o-mini), zero-shot, temperature = 0                                                                | GAP-T |
| Dataset         | GitHub open-source Java/Python, CC = 5–15, lọc bằng Lizard + Radon, loại bỏ getter/setter (< 5 SLOC)                  | GAP-D |
| Metric pipeline | Branch coverage đo bằng JaCoCo (Java) / coverage.py (Python); Mutation score đo bằng PIT (Java) / Cosmic-Ray (Python) | GAP-M |

**Prompt strategy:** Zero-shot. Không dùng CoT, không dùng method slicing (khác với Paper 1 HITS và Paper 4 SymPrompt — đây là điểm phân biệt). Temperature = 0 để reproducibility.

**Baseline pipeline:** Chạy Randoop trên cùng dataset → thu kết quả branch cov + mutation score → so sánh với GPT-4o mini output bằng Wilcoxon signed-rank.

**Student-written tests:** Thu thập từ bài tập lập trình trong môi trường học thuật (ví dụ: môn Software Testing, sinh viên viết test cho cùng function) → annotation manual → dùng làm ground truth human-level.

---

## Phân biệt với baseline của các paper trong SLR

| Paper              | Baseline của họ         | Baseline của nghiên cứu này            | Lý do khác                                                                    |
| ------------------ | ----------------------- | -------------------------------------- | ----------------------------------------------------------------------------- |
| HITS (Wang et al.) | EvoSuite + baseline LLM | Student-written tests + Randoop        | HITS dùng GPT-3.5 + method slicing; nghiên cứu này dùng GPT-4o mini zero-shot       |
| Tang et al.        | EvoSuite                | Randoop + student tests                | Tang et al. so với SBST; nghiên cứu này so với human và random                |
| Guerino & Vincenzi | Pynguin                 | Randoop + student tests                | Python only, code nhỏ (32.2 SLOC); nghiên cứu này CC 5–15, cả Java lẫn Python |
| ULT Bench          | PLT (leaked benchmark)  | Dataset mới CC 5–15 không từ benchmark | Nghiên cứu này không dùng Defects4J hoặc SF110 để tránh data contamination    |
