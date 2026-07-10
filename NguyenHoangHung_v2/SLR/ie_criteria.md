# IE Criteria – LLM for Unit Test Case Generation
**Thành viên:** Nguyễn Hùng (SE180765)
**PICO:** P=[Java/Python functions với cyclomatic complexity 5–15] | I=[GPT-4 zero-shot] | C=[student-written tests và Randoop] | O=[branch coverage ≥80%, mutation score ≥60%]

---

## Inclusion Criteria (IC)

| Mã | Tiêu chí |
|----|-----------|
| **IC-L** | Viết bằng tiếng Anh |
| **IC-Y** | Xuất bản từ năm 2020 trở đi |
| **IC-V** | Đăng trên conference hoặc journal — không phải blog, thesis, báo cáo kỹ thuật nội bộ, preprint |
| **IC-P** | Về task: sinh test case tự động (unit test, acceptance test, Gherkin/BDD) từ code hoặc requirement |
| **IC-I** | Dùng kỹ thuật LLM, NLP, hoặc AI-based (GPT, BERT, T5, LLaMA và tương đương) |
| **IC-R** | Có ít nhất 1 con số kết quả trong Table hoặc Figure của paper gốc (coverage, score, pass rate...) |
| **IC-Lang** | Thực nghiệm trên Java hoặc Python (không phải đa ngôn ngữ chung chung hoặc ngôn ngữ khác) |
| **IC-M** | Báo cáo branch coverage hoặc mutation score cụ thể (không chỉ line coverage hoặc pass rate đơn thuần) |
| **IC-T** | LLM là thành phần chính trực tiếp sinh test case — không phải agent framework, reinforcement learning, hoặc multi-agent phức tạp |

---

## Exclusion Criteria (EC)

| Mã | Tiêu chí |
|----|-----------|
| **EC-D** | Trùng lặp với paper đã có trong danh sách |
| **EC-A** | Không truy cập được full-text |
| **EC-S** | Dưới 4 trang (abstract, poster, short paper không có kết quả thực nghiệm) |
| **EC-P** | Không có thực nghiệm (position paper, vision paper, tutorial) |
| **EC-O** | Không về topic: test execution, debugging, maintenance; code gen không liên quan đến test |
