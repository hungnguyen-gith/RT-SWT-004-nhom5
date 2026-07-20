III. Results and Discussion

A. Branch Coverage
The experimental results reveal a clear performance difference between GPT-4o mini and Pynguin.

Across the benchmark of 50 Python functions, GPT-4o mini obtained a median Branch Coverage of 0%, whereas Pynguin achieved a median Branch Coverage of 50%. These results indicate that the search-based testing strategy employed by Pynguin was substantially more effective at exploring executable program paths than zero-shot LLM prompting.

Although GPT-4o mini successfully generated executable test files for most benchmark functions, the generated tests frequently failed to exercise meaningful execution branches. Consequently, executable tests did not necessarily translate into effective structural coverage.

B. Completion Success
GPT-4o mini successfully produced executable unit tests for 98% of the benchmark functions. This demonstrates that the model is capable of generating syntactically valid Python test code with high reliability. However, successful code generation alone was insufficient to achieve satisfactory testing effectiveness, as reflected by the branch coverage results.

C. Mutation Analysis
Mutation testing showed that both GPT-4o mini and Pynguin obtained a 0% Mutation Score on the benchmark dataset. This finding suggests that neither approach generated test suites capable of detecting the injected mutants under the current experimental setting.

The results also indicate that higher branch coverage does not necessarily imply stronger fault detection capability. Structural coverage and mutation testing evaluate different aspects of test quality and therefore should be considered complementary evaluation metrics.

D. Discussion
Overall, Pynguin consistently outperformed GPT-4o mini with respect to Branch Coverage because its search-based algorithm systematically explores execution paths during test generation. In contrast, GPT-4o mini relied solely on zero-shot prompting without iterative feedback or execution guidance, often producing tests that executed successfully but covered few meaningful branches.

These findings suggest that lightweight LLMs operating in a zero-shot setting remain insufficient as standalone solutions for automated Python unit testing. Nevertheless, the high completion success rate indicates that LLMs possess considerable potential as assistants for developers, particularly when integrated with search-based testing techniques or feedback-driven refinement strategies.