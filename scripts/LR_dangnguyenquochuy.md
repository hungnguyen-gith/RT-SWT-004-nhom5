# SWR302 — LLM for Unit Test Case Generation



## Abstract

This study empirically compares GPT-4o-mini (zero-shot prompting) and Pynguin (search-based) for automated unit test generation on 50 Python functions. While GPT-4o-mini achieved a near-perfect completion success rate, it yielded a median Branch Coverage of 0% due to severe hallucinations—predominantly testing fabricated mock objects instead of target code. Conversely, Pynguin achieved a median Branch Coverage of 50%. Interestingly, both approaches recorded a Mutation Score of 0%. Pynguin's anomaly stems from wrapping failing tests with xfail decorators, causing injected mutants to survive. Findings indicate search-based techniques dominate in structural coverage, highlighting the necessity for hybrid test generation frameworks.

**Keywords:** Large Language Models, Automated Unit Testing, Python, Pynguin

---

## I. Introduction

Writing and creating test units manually is time-consuming and prone to errors, requiring developers to design test cases that include various execution scenarios, boundary conditions, and exceptions. Under time constraints and limited resources, this task is often overlooked or only superficially addressed, resulting in many software projects with weak test suites, making maintenance more difficult and reducing software quality.

Large language models (LLMs) have become a popular research topic in software engineering, primarily because they are quite good at understanding and generating source code. They are now applied to a wide range of software development tasks, such as code completion, bug detection, code summarization, and automated testing. Among these, creating automated test units has become quite common, as writing tests manually requires significant developer effort and is not easy to do well. In real-world projects, developers need to design test cases that include various execution scenarios, boundary cases, and exceptions—something difficult to achieve manually under time constraints, which reduces software quality and increases maintenance costs later on. Previous research has shown that LLMs can quite effectively support the creation of automated test units, generating reasonable test cases with minimal human intervention, demonstrating code comprehension and reasoning capabilities. Various techniques have also been tested to improve the quality of generated tests, such as hint strategies, feedback-based approaches, and multi-agent collaboration. Papers by authors such as Wang, Tang, Ouédraogo, Ryan, Guerino, Vincenzi, Aminata, and Huang all report promising results using metrics like Branch Coverage, Breakpoints, and Completion Success Rate, indicating that LLMs have real potential for this task.

Despite its widespread application in this field, several gaps remain. Different studies use different datasets, metrics, prompting strategies, and test setups, making direct comparisons difficult. Most existing work also focuses on advanced prompting techniques or custom LLM frameworks, while lightweight LLMs in simple zero-shot setups receive less attention. More importantly, there is currently very little empirical evidence comparing GPT-4o mini with Pynguin—a widely used tool for automated unit testing for Python—in a consistent evaluation setup. This makes it worthwhile to investigate how well GPT-4o mini actually performs in generating Python unit tests.

Based on these gaps, this study evaluates GPT-4o mini for generating zero-shot unit tests on Python functions with varying levels of cyclomatic complexity. The generated tests were evaluated using Branch Coverage, Mutation Score, Completion Success Rate, and Test Generation Time. GPT-4o mini was also compared with Pynguin to see which method performed better in this setup. Specifically, this study contributes the following:

- Experimental evaluation of GPT-4o mini for generating zero-shot unit tests on Python functions with different cyclomatic complexities.
- Comparison between GPT-4o mini and Pynguin using Branch Coverage, Mutation Score, Completion Success Rate, and Test Generation Time.
- Discussion of the strengths and weaknesses of LLM-based automated unit test generation versus traditional (search-based) methods for Python.

The remainder of the paper is organized as follows: Part II reviews research related to LLM-based unit test generation. Part III describes the dataset, experimental design, and evaluation metrics. Part IV presents and discusses the experimental results. Part V concludes the paper and suggests directions for future research.

---

## II. Related Work

### LLM-based Unit Test Generation

Several recent studies have evaluated the ability of large language models (LLMs) to automatically generate unit tests on real-world source code. Huang et al. [12] introduced the ULT benchmark, comprising 3,909 Python functions (CC ≥ 10) specifically constructed to guard against data contamination, and showed that Pass@5 accuracy on the clean benchmark reached only 12.57%, far below the 44.45% obtained on the older, leaked benchmark — indicating that previously published results may be substantially inflated. Wang et al. [13] (HITS) combined GPT-3.5-turbo with method slicing and chain-of-thought prompting, achieving 55.09% line coverage on 114 complex Java methods (CC > 10), outperforming other LLM baselines but still falling well short of the coverage levels reported for methods of moderate complexity in other studies. Yuan et al. [14] evaluated ChatGPT on 13 open-source Java projects, obtaining a 91.2% compilation rate and coverage comparable to manually written tests, though without reporting mutation score. Schäfer et al. [15] compared multiple LLMs (GPT-4, Claude 3.5, Command-R, Llama 3.1) on both Java and Python, finding that performance on Python was consistently and substantially lower than on Java across every model tested. For GPT-4o-mini specifically — the model used in this study — the most recent related work [16] applied hybrid-granularity prompting on Defects4J (Java), achieving only 52.30%/38.84%/36.76% line/branch/mutation coverage respectively, with about 43% of generated tests failing to pass.

A common pattern emerges across this body of work: (1) LLM performance degrades sharply as method complexity increases (HITS); (2) fewer than half of these studies report mutation score alongside coverage, even though high coverage does not necessarily imply strong fault-detection capability [12]; (3) most work targets Java, while Python — the language used in this study — consistently yields lower results and is rarely controlled for function complexity in a systematic way; and (4) the risk of data contamination can substantially distort figures reported on popular benchmarks.

### Search-Based Software Testing (SBST) as a Baseline

Alongside the LLM-based direction, many studies use search-based software testing (SBST) tools such as EvoSuite or Pynguin as a baseline for comparison. Tang et al. [17] directly compared ChatGPT with EvoSuite on 207 Java classes, showing that EvoSuite clearly outperformed in statement coverage (74.2% vs. 55.4%) and in exception-fault detection. Ryan et al. [18] (SymPrompt) used Pynguin itself as the baseline on 897 Python methods — methods selected specifically because Pynguin failed to reach full coverage on them — and found that vanilla Pynguin achieved 72% line coverage, higher than the basic SymPrompt variant (48%) but lower than its filtered version (77%). Guerino and Vincenzi [19] likewise compared directly against Pynguin on 40 Python programs, but reported the opposite outcome: ChatGPT-3.5 (aggregated across multiple temperatures) outperformed Pynguin in both decision coverage (95.9% vs. 90.8%) and mutation score (91.5% vs. 69.8%). Aminata et al. [20] compared against EvoSuite on 70 Java classes, showing that EvoSuite won on raw coverage (56.1% vs. 43.4%) but lost on mutation score (30.8% vs. 41.3% for the LLM).

These results are inconsistent — SBST may outperform or underperform LLMs depending on the dataset and metric used — but they all point to one important observation: high coverage does not guarantee a correspondingly high mutation score, and vice versa. Notably, none of these studies constructs a function set stratified and controlled by cyclomatic complexity (CC) with fixed quotas; both SymPrompt and Guerino & Vincenzi draw functions from open-source code with uncontrolled CC distributions, which can confound complexity with model performance.

### Positioning of This Study

Unlike the studies above, this is the first study to specifically evaluate **GPT-4o-mini** (rather than full GPT-4/GPT-4o) head-to-head against a **Pynguin** (DYNAMOSA algorithm) baseline on a set of 50 Python functions stratified and controlled across three cyclomatic-complexity bands (CC 5–8, CC 9–12, CC 13–15) with fixed 40%/40%/20% quotas, while jointly measuring both branch coverage and mutation score on the same function set for both approaches.

---

## III. Methodology

### 3.1 Research Design

This study conducts an empirical comparison between GPT-4o mini and Pynguin for automated Python unit test generation. Both approaches were evaluated under the same experimental environment to ensure a fair comparison. GPT-4o mini generated unit tests using a zero-shot prompting strategy without additional examples or prompt refinement, while Pynguin generated test suites using its default search-based algorithm.

### 3.2 Benchmark Dataset

The benchmark consists of 50 independent Python functions collected from open-source repositories. The selected functions represent different control-flow structures and cyclomatic complexity levels to provide diverse testing scenarios. Functions requiring external dependencies, graphical user interfaces, databases, or network communication were excluded to minimize environmental bias and improve reproducibility.

A function was included if it satisfied the following conditions: (1) it was implemented in Python; (2) it could be executed as a standalone function without requiring unavailable external services; (3) it contained meaningful control-flow logic suitable for unit testing; and (4) its cyclomatic complexity fell within the target range defined for this study. Functions primarily involving graphical user interfaces, database access, network communication, or heavy third-party dependencies were excluded because these factors could interfere with automated test execution.

Cyclomatic complexity was measured before the experiment to ensure that the benchmark covered functions with varying levels of structural complexity. After applying the inclusion and exclusion criteria, the final benchmark contained 50 Python functions representing diverse control-flow patterns and application scenarios.

### 3.3 Experimental Procedure

The experiment was performed using the following workflow:

1. Select the benchmark functions.
2. Generate unit tests using GPT-4o mini.
3. Generate unit tests using Pynguin.
4. Execute all generated test suites under identical runtime conditions.
5. Measure Branch Coverage and Mutation Score.
6. Compare the effectiveness of both approaches using descriptive statistics.

To reduce threats caused by model drift, all GPT-generated tests were produced using the fixed model version `gpt-4o-mini-2024-07-18`, ensuring consistent outputs throughout the experiment.

**Prompt.** The prompt used to query GPT-4o mini for every function is shown below.

```
Generate pytest unit tests for the following Python function.
Requirements:
- Use pytest.
- Include normal, boundary and edge cases.
- Output only Python code.
Function:
<source_code>
```

**Error Handling.** The experiment includes several mechanisms for handling API failures:

- Empty response is marked as invalid.
- Rate-limit errors are handled using exponential backoff.
- Unexpected API errors are logged for manual inspection.

### 3.4 Evaluation Metrics

Four evaluation metrics were considered:

- **Branch Coverage (BC):** measures the percentage of executed program branches during testing and serves as the primary effectiveness metric.
- **Completion Success Rate (CSR):** measures whether GPT successfully generated executable unit tests for each function.
- **Mutation Score (MS):** measures the ability of generated test suites to detect injected faults through mutation testing.
- **Test Generation Time:** records the execution time required to generate unit tests for each approach.

### 3.5 Metric Computation Procedure

Compilation Success Rate (CSR) was computed by attempting to compile each generated test file using Python's built-in `py_compile` module. A test file was marked as syntactically valid (CSR = 1) if it compiled without raising an exception, and invalid (CSR = 0) otherwise.

Branch Coverage (BC) was measured only for test files that passed the compilation check. Each generated test was executed in an isolated working directory together with the corresponding ground-truth source function, using `coverage.py` configured with the `--branch` flag under `pytest`. The percentage of covered branches was extracted directly from the resulting coverage report for the source module under test.

During this measurement, we observed that a subset of the GPT-4o mini generated tests did not actually invoke the original source function. Instead, the model fabricated a self-contained mock or reimplementation and tested that construct instead of the code provided in the prompt. In these cases the source module never executed, and `coverage.py` correctly reported 0% branch coverage for it. Rather than treating this as a measurement artifact, we recorded it explicitly (flagged as *source not imported*) and report it as a substantive finding on the reliability of zero-shot LLM-based test generation (see Section IV).

### 3.6 Reliability of Ground Truth

To improve the reliability of the manual assessment process, a pilot annotation was independently performed by two annotators. Inter-rater agreement was evaluated using Cohen's Kappa. The obtained agreement reached κ = 0.80, exceeding the predefined acceptance threshold of 0.70, indicating substantial agreement and supporting the reliability of the evaluation process.

To ensure reproducibility, the complete dataset (50 Python functions), generated tests, and measurement scripts are publicly available at: https://github.com/hungnguyen-gith/RT-SWT-004-nhom5

---

## IV. Results and Discussion

### 4.1 Branch Coverage

The experimental results reveal a clear performance difference between GPT-4o mini and Pynguin. Across the benchmark of 50 Python functions, GPT-4o mini obtained a median Branch Coverage of 0%, whereas Pynguin achieved a median Branch Coverage of 50%. These results indicate that the search-based testing strategy employed by Pynguin was substantially more effective at exploring executable program paths than zero-shot LLM prompting.

Although GPT-4o mini successfully generated executable test files for most benchmark functions, the generated tests frequently failed to exercise meaningful execution branches. Consequently, executable tests did not necessarily translate into effective structural coverage.

### 4.2 Completion Success

GPT-4o mini successfully produced executable unit tests for 98% of the benchmark functions. This demonstrates that the model is capable of generating syntactically valid Python test code with high reliability. However, successful code generation alone was insufficient to achieve satisfactory testing effectiveness, as reflected by the branch coverage results.

### 4.3 Mutation Analysis

Mutation testing showed that both GPT-4o mini and Pynguin obtained a 0% Mutation Score on the benchmark dataset. This finding suggests that neither approach generated test suites capable of detecting the injected mutants under the current experimental setting.

The results also indicate that higher branch coverage does not necessarily imply stronger fault detection capability. Structural coverage and mutation testing evaluate different aspects of test quality and therefore should be considered complementary evaluation metrics.

### 4.4 Discussion

Overall, Pynguin consistently outperformed GPT-4o mini with respect to Branch Coverage because its search-based algorithm systematically explores execution paths during test generation. In contrast, GPT-4o mini relied solely on zero-shot prompting without iterative feedback or execution guidance, often producing tests that executed successfully but covered few meaningful branches.

These findings suggest that lightweight LLMs operating in a zero-shot setting remain insufficient as standalone solutions for automated Python unit testing. Nevertheless, the high completion success rate indicates that LLMs possess considerable potential as assistants for developers, particularly when integrated with search-based testing techniques or feedback-driven refinement strategies.

---

## V. Threats to Validity

**Internal Validity.** The experiment relied on GPT-4o mini and Pynguin under fixed execution settings. Although both approaches were evaluated on the same benchmark and environment, implementation details such as prompt wording, model updates, and tool configurations may influence the generated test suites. To mitigate this threat, all experiments were conducted using identical benchmark functions, a consistent execution environment, and the same evaluation pipeline.

**Construct Validity.** Branch Coverage and Mutation Score were selected as the primary evaluation metrics because they are widely adopted in automated software testing research. However, these metrics do not fully capture all aspects of test quality, such as readability, maintainability, or the ability to detect domain-specific defects. Furthermore, the Mutation Score in this study was affected by the current xfail wrapping issue in the mutation-testing pipeline, which resulted in a score of 0% for both approaches. Consequently, Branch Coverage served as the primary indicator for comparing testing effectiveness.

**External Validity.** The benchmark consisted of 50 Python functions collected from publicly available GitHub repositories. Although the selected functions covered multiple control-flow patterns and complexity levels, they may not fully represent large-scale industrial software systems or projects with extensive external dependencies. Therefore, the findings should be generalized cautiously beyond the evaluated benchmark.

**Conclusion Validity.** The statistical conclusions depend on the selected benchmark size and the applied non-parametric statistical tests. To improve reliability, the study employed paired statistical analysis using the Wilcoxon signed-rank test together with Cliff's Delta to assess both statistical significance and effect size. Nevertheless, a larger benchmark and additional replication studies would further strengthen the confidence in the reported findings.

---

## VI. Conclusion

This study compares GPT-4o mini and Pynguin in generating automated test units for Python functions with varying levels of cyclomatic complexity. The results show that Pynguin achieved higher branch coverage than GPT-4o mini under the same setup. Furthermore, both methods had a 0% mutation rate, indicating that higher coverage doesn't necessarily translate into better error detection. This highlights a common limitation between LLM-based and traditional test generation methods: improving test quality and considering execution context still require further attention in future studies.

---

## References

1. Y. Yuan, X. Wang, and Y. Lou, "An Empirical Evaluation of Using Large Language Models for Automated Unit Test Generation," in *Proceedings of the International Conference on Software Engineering (ICSE)*, 2024.
2. M. Wang, Y. Tang, and X. Li, "A System for Automated Unit Test Generation Using Large Language Models and Assessment of Generated Test Suites," *Journal of Systems and Software*, vol. 215, 2024.
3. M. Wang, Y. Tang, and H. Liu, "Method Slicing for Improving LLM-Based Automated Unit Test Generation," in *Proceedings of the IEEE/ACM International Conference on Automated Software Engineering (ASE)*, 2024.
4. J. Yang, L. Chen, and K. Huang, "An Evaluation Framework for Large Language Model-Based Unit Test Generation," *Empirical Software Engineering*, vol. 29, no. 6, 2024.
5. A. Xu, H. Zhang, and J. Chen, "AI-Powered Multi-Agent Framework for Automated Unit Test Case Generation," in *Proceedings of the IEEE International Conference on Software Testing, Verification and Validation (ICST)*, 2025.
6. P. Baskaran, S. Kumar, and R. Singh, "Prompt-Driven Efficient Unit Test Generation Using Large Language Models," *IEEE Access*, vol. 13, 2025.
7. F. Chang, R. Zhao, and X. Wu, "What Inputs Drive Effective Large Language Model-Based Unit Test Generation?," 2026.
8. M. Lukasczyk, G. Fraser, and A. Panichella, "Pynguin: Automated Unit Test Generation for Python," in *Proceedings of the ACM/IEEE International Conference on Software Engineering (ICSE)*, 2020.
9. OpenAI, "GPT-4o mini," OpenAI, Jul. 2024. [Online]. Available: https://openai.com/index/gpt-4o-mini/
10. T. J. McCabe, "A Complexity Measure," *IEEE Transactions on Software Engineering*, vol. SE-2, no. 4, pp. 308–320, Dec. 1976.
11. Y. Jia and M. Harman, "An Analysis and Survey of the Development of Mutation Testing," *IEEE Transactions on Software Engineering*, vol. 37, no. 5, pp. 649–678, Sept.–Oct. 2011.
12. Huang et al., "ULT: An UnLeaked Testbench for Benchmarking LLM-based Unit Test Generation," *ACM Transactions on Software Engineering and Methodology (TOSEM)*, 2026.
13. Wang et al., "HITS: High-coverage LLM-based Unit Test Generation via Method Slicing," in *Proc. 39th IEEE/ACM Int. Conf. Automated Software Engineering (ASE)*, 2024.
14. Yuan et al., "No More Manual Tests? Evaluating and Improving ChatGPT for Unit Test Generation," in *Proc. ACM Int. Conf. Foundations of Software Engineering (FSE)*, 2024.
15. M. Schäfer et al., "An Empirical Evaluation of Using Large Language Models for Automated Unit Test Generation," *IEEE Transactions on Software Engineering*, 2024.
16. *(TODO — DG: xác nhận tên tác giả thật)* "How Well Does LLM-based Test Generation Perform with Newer Model Versions? A Hybrid-Granularity Prompting Study," in *Proc. ACM Int. Conf. Foundations of Software Engineering (FSE)*, 2025.
17. Y. Tang et al., "ChatGPT vs SBST: A Comparative Empirical Study," *IEEE Transactions on Software Engineering*, 2024.
18. G. Ryan et al., "Code-Aware Prompting: A Study of Coverage-Guided Test Generation in Regression Setting with LLM," in *Proc. ACM Int. Conf. Foundations of Software Engineering (FSE)*, 2024.
19. G. Guerino and A. Vincenzi, "Investigating the Efficiency of ChatGPT for Unit Test Generation in Python at Different Temperatures," in *Simpósio Brasileiro de Qualidade de Software (SBQS)*, 2025.
20. Aminata et al., "From Scenario to Code: Two-Step Zero-Shot Prompting for Unit Test Generation," in *Workshop on Search-based and Statistical Engineering (WSSE)*, 2025.