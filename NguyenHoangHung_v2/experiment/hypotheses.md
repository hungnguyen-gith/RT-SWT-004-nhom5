# Hypotheses – LLM for Unit Test Case Generation

**Thành viên:** Nguyễn Hùng (SE180765)

---

## RQ1

**H0:** GPT-4o mini Zero-shot không đạt ít nhất một trong các điều kiện sau:

Mutation Score ≥ 40%
Branch Coverage ≥ 50%
Compilation Success Rate ≥ 80%.

**H1:** GPT-4o mini Zero-shot đạt đồng thời:

Mutation Score ≥ 40%
Branch Coverage ≥ 50%
Compilation Success Rate ≥ 80%

**Statistical test dự kiến:**

Nếu test theo từng class:

One-sample Wilcoxon Signed-Rank Test

So sánh:

Mutation Score thực tế vs ngưỡng 40%
Branch Coverage thực tế vs ngưỡng 50%

Compilation Success Rate:

One-sample Proportion Test (Binomial Test)

Kiểm tra:

CSR ≥ 80%
