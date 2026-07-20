II. Methodology

A. Research Design
This study conducts an empirical comparison between GPT-4o mini and Pynguin for automated Python unit test generation. Both approaches were evaluated under the same experimental environment to ensure a fair comparison. GPT-4o mini generated unit tests using a zero-shot prompting strategy without additional examples or prompt refinement, while Pynguin generated test suites using its default search-based algorithm.


B. Benchmark Dataset
The benchmark consists of 50 independent Python functions collected from open-source repositories. The selected functions represent different control-flow structures and cyclomatic complexity levels to provide diverse testing scenarios. Functions requiring external dependencies, graphical user interfaces, databases, or network communication were excluded to minimize environmental bias and improve reproducibility.

A function was included if it satisfied the following conditions: (1) it was implemented in Python; (2) it could be executed as a standalone function without requiring unavailable external services; (3) it contained meaningful control-flow logic suitable for unit testing; and (4) its cyclomatic complexity fell within the target range defined for this study. Functions primarily involving graphical user interfaces, database access, network communication, or heavy third-party dependencies were excluded because these factors could interfere with automated test execution.

Cyclomatic complexity was measured before the experiment to ensure that the benchmark covered functions with varying levels of structural complexity. After applying the inclusion and exclusion criteria, the final benchmark contained 50 Python functions representing diverse control-flow patterns and application scenarios.


C. Experimental Procedure
The experiment was performed using the following workflow:
- Select the benchmark functions.
- Generate unit tests using GPT-4o mini.
- Generate unit tests using Pynguin.
- Execute all generated test suites under identical runtime conditions.
- Measure Branch Coverage and Mutation Score.
- Compare the effectiveness of both approaches using descriptive statistics.
To reduce threats caused by model drift, all GPT-generated tests were produced using the fixed model version gpt-4o-mini-2024-07-18, ensuring consistent outputs throughout the experiment.

D. Evaluation Metrics
Four evaluation metrics were considered.

Branch Coverage (BC): measures the percentage of executed program branches during testing and serves as the primary effectiveness metric.

Completion Success Rate (CSR): measures whether GPT successfully generated executable unit tests for each function.

Mutation Score (MS): measures the ability of generated test suites to detect injected faults through mutation testing.

Test Generation Time: records the execution time required to generate unit tests for each approach.


E. Reliability of Ground Truth
To improve the reliability of the manual assessment process, a pilot annotation was independently performed by two annotators. Inter-rater agreement was evaluated using Cohen's Kappa. The obtained agreement reached κ = 0.80, exceeding the predefined acceptance threshold of 0.70, indicating substantial agreement and supporting the reliability of the evaluation process.

F. Fingures and Tables