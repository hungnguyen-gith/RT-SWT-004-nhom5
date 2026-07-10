# Hypotheses Draft – LLM for Unit Test Case Generation

Ngày: 2026-06-11

---

## RQ1 – Branch Coverage & Mutation Score so với Student-Written Tests

**RQ1 (tên ngắn):** GPT-4o mini zero-shot vs. Student-written tests

H0₁: GPT-4o mini zero-shot KHÔNG đạt [Branch Coverage ≥ 50%] AND [Mutation Score ≥ 40%] AND [Compilation Success Rate ≥ 80%] so với student-written tests trên Java/Python functions có CC = 5–15.

H1₁: GPT-4o mini zero-shot ĐẠT [Branch Coverage ≥ 50%] AND [Mutation Score ≥ 40%] AND [Compilation Success Rate ≥ 80%] so với student-written tests trên Java/Python functions có CC = 5–15.

Statistical test dự kiến: Wilcoxon signed-rank (α = 0.05) — output branch coverage là điểm số liên tục; Binomial exact test cho pass rate (tỉ lệ test suite compile được và pass).

> **Lưu ý threshold RQ1:** Branch Coverage ≥ 50% derive từ Case 1 — floor từ literature LLM: HITS 48.12%, SymPrompt 44%, ULT 30.22%, 2SZSP 31.3% → ceiling 50% (cao hơn trung bình, vẫn khả thi với GPT-4o mini). Mutation Score ≥ 40% derive từ Case 1 — floor từ literature LLM: HITS 36.25%, ULT 33.59%, 2SZSP 30.8% → ceiling 40% (vượt mức trung bình, cao hơn random < 30%). Xem chi tiết tại design-rationale.md.

---

## RQ2 – So với Randoop

**RQ2 (tên ngắn):** GPT-4o mini zero-shot vs. Randoop

H0₂: GPT-4o mini zero-shot KHÔNG tốt hơn [Randoop] về [Branch Coverage] và [Mutation Score] trên Java/Python functions có CC = 5–15.

H1₂: GPT-4o mini zero-shot TỐT HƠN [Randoop] về [Branch Coverage] và [Mutation Score] trên Java/Python functions có CC = 5–15.

Statistical test dự kiến: Wilcoxon signed-rank (α = 0.05) cho branch coverage (liên tục); Mann-Whitney U nếu so sánh 2 nhóm độc lập (GPT-4o mini vs Randoop output không paired).

> **Lưu ý threshold RQ2:** Threshold cụ thể TBD — sẽ derive từ pilot run Randoop trên 5–10 sample functions (Case 2: floor value). Amendment sẽ được ghi sau pilot tuần 7.
