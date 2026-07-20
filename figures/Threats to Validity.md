V. Threats to Validity

This study has several limitations that should be considered when interpreting the experimental results.

A. Internal Validity
   The experiment relied on GPT-4o mini and Pynguin under fixed execution settings. Although both approaches were evaluated on the same benchmark and environment, implementation details such as prompt wording, model updates, and tool configurations may influence the generated test suites. To mitigate this threat, all experiments were conducted using identical benchmark functions, a consistent execution environment, and the same evaluation pipeline.

B. Construct Validity
   Branch Coverage and Mutation Score were selected as the primary evaluation metrics because they are widely adopted in automated software testing research. However, these metrics do not fully capture all aspects of test quality, such as readability, maintainability, or the ability to detect domain-specific defects. Furthermore, the Mutation Score in this study was affected by the current xfail wrapping issue in the mutation-testing pipeline, which resulted in a score of 0% for both approaches. Consequently, Branch Coverage served as the primary indicator for comparing testing effectiveness.

C. External Validity
   The benchmark consisted of 50 Python functions collected from publicly available GitHub repositories. Although the selected functions covered multiple control-flow patterns and complexity levels, they may not fully represent large-scale industrial software systems or projects with extensive external dependencies. Therefore, the findings should be generalized cautiously beyond the evaluated benchmark.

D. Conclusion Validity
   The statistical conclusions depend on the selected benchmark size and the applied non-parametric statistical tests. To improve reliability, the study employed paired statistical analysis using the Wilcoxon signed-rank test together with Cliff's Delta to assess both statistical significance and effect size. Nevertheless, a larger benchmark and additional replication studies would further strengthen the confidence in the reported findings.