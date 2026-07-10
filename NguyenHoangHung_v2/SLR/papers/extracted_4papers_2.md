# Tổng hợp thông tin từ 4 PDF mới — Phục vụ Evidence Table
> Mỗi mục ghi rõ: nguồn (tên paper + trang PDF)

---

## Paper 5 — Guerino & Vincenzi, 2025 — ChatGPT Python (SBQS '25)
**Full title:** Exploring ChatGPT Efficiency in Automatic Test Generation for Python: A Comparative Analysis  
**Authors:** Lucca Renato Guerino, Auri Marcelo Rizzo Vincenzi  
**Venue:** SBQS '25 (XXIV Brazilian Symposium on Software Quality), Nov 04–07, 2025, São José dos Campos, SP  
**DOI/URL:** https://sol.sbc.org.br/index.php/sbqs/article/view/38998  
**Artifact:** https://github.com/aurimrv/python_experiments2

### Tool / Approach
- **ChatGPT-3.5-turbo** via OpenAI API
- Zero-shot prompting: system prompt "You are a senior software tester specialized in mutation testing", user prompt yêu cầu tạo test Pytest format cho từng module
- Error-feedback loop: tối đa 3 lần correction nếu test fail
- 11 temperature settings (0.0 → 1.0, bước 0.1), 30 test sets/temperature/program → **330 test sets/program**
- Coverage đo bằng **Coverage.py** (decision/branch coverage)
- Mutation testing: **MutPy** và **Cosmic-Ray**
- Baseline: **Pynguin** (DynaMOSA, MIO, MOSA, Whole-Suite) + **pre-existing test sets**
- [Nguồn: p.2–4 — Sec.4, Listing 1–2, Fig.1]

### Dataset
- **40 Python programs** từ GitHub repositories (clair3st/Data-Structures, keon/algorithms, exterkamp/Python-Data-Structures)
- Tiêu chí: implemented in Python + có pre-existing test set (UnitTest hoặc Pytest)
- Đặc điểm dataset: 22 ST (Structural) + 18 OO (Object-Oriented); avg 4.3 methods/functions; avg cyclomatic complexity 4.6; avg 32.2 SLOC
- Các programs gồm: breadth_first_search, binary_search_tree, dijkstras, linked_list, mergesort, v.v. (xem Table 1)
- [Nguồn: p.3 — Table 1, Sec.4]

### Metrics
- **Decision coverage** (branch coverage) — đo bằng Coverage.py
- **MutPy mutation score** — tỉ lệ mutants bị killed
- **Cosmic-Ray mutation score** — tỉ lệ mutants bị killed
- Success rate (% test sets pass Pytest validation)
- Token cost (OpenAI API)
- [Nguồn: p.2–3 — Sec.4 (Metrics)]

### Kết quả chính — Decision Coverage (Table 4, p.6–7)

| Phương pháp | Avg. Decision Coverage |
|-------------|----------------------|
| LLM ALL (tất cả temperatures gộp) | **95.9%** |
| Pre-existing tests | 94.8% |
| Pynguin | 90.8% |
| LLM best single temp (0.6) | 86.1% |
| LLM worst single temp (0.0) | 56.4% |

- Khi **gộp tất cả test sets từ mọi temperatures** ("LLM ALL"), ChatGPT **vượt Pynguin (95.9% vs 90.8%)** và gần bằng pre-existing tests (94.8%) về decision coverage
- Temperature 0.6 cho avg coverage tốt nhất trong các temperature đơn lẻ: **86.1%** (SD = 20.9)
- P12 (edit_distance.py): **0%** — ChatGPT không generate được test hợp lệ cho program này
- [Nguồn: p.6–7 — Table 4, Sec.6]

### Kết quả chính — MutPy Mutation Score (Table 5, p.7–8)

| Phương pháp | Avg. MutPy Score |
|-------------|-----------------|
| LLM ALL | **91.5%** |
| Pre-existing tests | 87.9% |
| Pynguin | 69.8% |
| LLM best single temp (0.6) | 85.9% |

- LLM (combined ALL) **vượt cả Pynguin và pre-existing tests** về MutPy mutation score
- LLM best single temperature (0.6): 85.9% vs Pynguin 69.8% → LLM **vượt Pynguin 16.1 pp**
- Pre-existing tests chỉ nhỉnh hơn LLM best single temp **~2.03%**
- [Nguồn: p.7–8 — Table 5, Sec.6]

### Kết quả chính — Cosmic-Ray Mutation Score (Table 6, p.8–9)

| Phương pháp | Avg. Cosmic-Ray Score |
|-------------|----------------------|
| LLM ALL | **86.9%** |
| Pre-existing tests | 85.6% |
| Pynguin | 70.8% |
| LLM best single temp (0.6) | 76.9% |

- Tương tự MutPy: LLM ALL **vượt cả Pynguin và pre-existing** về Cosmic-Ray score
- Cosmic-Ray scores nhìn chung thấp hơn MutPy do Cosmic-Ray tạo mutants tinh tế hơn
- [Nguồn: p.8–9 — Table 6, Sec.6]

### Kết quả chính — Success Rate (Table 2, p.5)
- **Overall avg success rate: 27.73%** (tính cả các programs có 0% success)
- **43.97%** khi loại bỏ các programs có 0% success
- Temperature 1.0 cho avg success rate cao nhất: **43.33%**; temperature 0.6 cũng cao: **36.67%**
- 39/40 programs generate được valid test ít nhất ở 1 temperature; P12 (edit_distance.py) = 0% ở tất cả temperatures
- [Nguồn: p.5 — Table 2, Sec.6]

### Kết quả chính — Fault Detection Capability (RQ3, Tables 7–8, p.8–9)
- MutPy operators dễ detect: SIR (0.99), SDI (0.93), LOR (0.94), EHD (0.92), ZIL (0.90), SVD (0.90)
- MutPy operators khó detect: EXS (0.06), LCR (0.53), BCR (0.63)
- Cosmic-Ray operators dễ: ReplaceBinaryOperator_BitAnd_Add (1.00), Sub_Div (0.98), ZeroIterationForLoop (0.94)
- Cosmic-Ray operators khó: ReplaceComparisonOperator_Is_Eq (0.00), IsNot_NotEq (0.00), ReplaceAndWithOr (0.38)
- LLM tests yếu ở: identity checks, control flow (break/continue), subtle comparison mutations
- [Nguồn: p.8–9 — Table 7, Table 8, Sec.6]

### Hạn chế
- Chỉ Python; chỉ ChatGPT-3.5-turbo (không phải GPT-4)
- 40 programs đơn giản (avg 32.2 SLOC, avg CC 4.6) — không đại diện đầy đủ real-world
- Single prompt cho tất cả programs; không thử nhiều LLM
- P38 (stack.py): Cosmic-Ray không tạo được mutants
- [Nguồn: p.9–10 — Sec.7, Sec.8]

---

## Paper 6 — Aminata et al., 2025 — Scenario to Code / 2SZSP (WSSE '25)
**Full title:** From Scenario to Code: Structured Prompting for LLM-Based Unit Test Generation  
**Authors:** Aminata Diop, Fadel Toure, Mourad Badri (Université du Québec à Trois-Rivières)  
**Venue:** WSSE 2025 (7th World Symposium on Software Engineering), Oct 24–26, 2025, Okayama, Japan  
**DOI:** https://doi.org/10.1145/3779657.3779658

### Tool / Approach
- **Two-Step Zero-Shot Prompting (2SZSP)** với **Mistral 7B**
- Bước 1 (Step 1 — Scenario Identification): Prompt Mistral 7B liệt kê tối đa 5 test scenarios cho từng method (xem Figure 1, p.4)
- Bước 2 (Step 2 — Test Code Generation): Prompt generate JUnit 5 test code cho từng scenario đã identify (xem Figure 2, p.4); system message yêu cầu: không call private methods/variables, không dùng mock, tuân theo AAA pattern, import đầy đủ
- Mistral 7B chọn vì: sliding window attention (xử lý long prompt tốt), open-source (reproducibility), competitive performance trên code tasks
- Framework: JUnit 5
- Evaluation platform: **JUGE** (Java Unit test Generator Evaluation infrastructure)
- Comparison tool: **EvoSuite**
- [Nguồn: p.2–4 — Sec.3, Sec.3.1, Sec.3.2, Fig.1, Fig.2]

### Dataset
- **4 Java projects từ SBST 2020 benchmark**: GUAVA, SPOON, PDFBOX, FESCAR/Seata
- Lọc subset: **70 classes** tổng cộng (20 từ GUAVA, 20 từ FESCAR, 20 từ PDFBOX, 10 từ SPOON)
- Thống kê (Table 1, p.4):
  - FESCAR: 20 classes, 490 branches, Mean 24.5, SD 27.3
  - GUAVA: 20 classes, 926 branches, Mean 46.3, SD 61.5
  - PDFBOX: 20 classes, 1070 branches, Mean 53.5, SD 75.6
  - SPOON: 10 classes, 1072 branches, Mean 107.2, SD 12.9
- Các classes được lọc từ original projects dựa trên complexity và compatibility
- [Nguồn: p.3–4 — Sec.4.1, Table 1]

### Metrics
- **Line Coverage** (% executable lines covered) — đo bằng JUGE
- **Branch Coverage** (% branches covered) — đo bằng JUGE
- **Mutation Score** (% mutants killed) — đo bằng JUGE (mutation analysis)
- [Nguồn: p.5 — Sec.4.2]

### Kết quả chính (Table 2, p.5)

| Metrics | EvoSuite | **2SZSP (Mistral 7B)** |
|---------|----------|----------------------|
| Line Coverage (%) | **56.1** | 43.4 |
| Branch Coverage (%) | **49.5** | 31.3 |
| Mutation Score (%) | 30.8 | **41.3** |

- **EvoSuite** đạt line coverage cao hơn 2SZSP: **+12.7 pp** (56.1% vs 43.4%)
- **EvoSuite** đạt branch coverage cao hơn 2SZSP: **+18.2 pp** (49.5% vs 31.3%)
- **2SZSP vượt EvoSuite về mutation score: +10.5 pp** (41.3% vs 30.8%) — sự khác biệt đáng kể
- Khoảng **64% generated tests không compile** — hạn chế lớn nhất
- [Nguồn: p.5 — Table 2, Sec.4.3, Sec.5.1]

### Hạn chế
- Chỉ Java; chỉ Mistral 7B (không GPT-4)
- **~64% tests không compile** — tỉ lệ non-compilable cao
- Dataset hạn chế: 70 classes từ 4 projects
- Không dùng mock → hạn chế test complex classes với dependencies
- Zero-shot prompting nhạy cảm với wording → prompt engineering phức tạp
- LLM hallucination (method calls không tồn tại, API misuse, assertions sai logic)
- [Nguồn: p.6–7 — Sec.5.2, Sec.5.3]

---

## Paper 7 — Cabral et al., 2025 — ChatGPT vs DeepSeek (SBQS '25)
**Full title:** Evaluating LLM-Generated Unit Tests with Mutation Testing: ChatGPT vs DeepSeek  
**Authors:** Pedro Fernando Marinho Cabral, João Pedro Souza Arruda, Cleidson Ronald Botelho de Souza, Victor Hugo Santiago Costa Pinto (Federal University of Pará — UFPA)  
**Venue:** SBQS '25, Nov 04–07, 2025, São José dos Campos, SP  
**DOI/URL:** https://sol.sbc.org.br/index.php/sbqs/article/view/39001  
**Artifact:** https://doi.org/10.5281/zenodo.17250744

### Tool / Approach
- **ChatGPT (GPT-4o)** vs **DeepSeek Chat V3**
- Zero-shot prompting tại class level: mỗi prompt được execute **5 lần/class** (new conversation mỗi lần để tránh context history)
- Prompt yêu cầu: tests viết bằng Java/JUnit 5, tuân naming best practices, cover nhiều scenarios, tối đa hoá mutation score, model đóng vai experienced test professional
- Mutation tool: **PIT (Pitest)** — inject bytecode mutants; 1 fixed set mutants/class (tất cả test suites dùng cùng set)
- Default PIT operators; không detect equivalent mutants
- Chỉ test suites compile + 100% pass rate mới eligible cho mutation testing
- Metrics: Compilation Success Rate (CSR), Mutation Coverage (MC), Mutation Score (MS)
- Statistical test: Spearman correlation (ρ) cho RQ1; t-test cho RQ3
- [Nguồn: p.3–5 — Sec.4.2, Sec.4.3, Sec.4.4, Sec.4.5]

### Dataset
- **6 Java classes từ Defects4J benchmark** (3 projects)
- Chọn theo: diversity in code structure, methods suitable for unit testing, variation in cyclomatic complexity (đo bằng SonarQube)
- Chi tiết (Table 1, p.4):

| Class | Project | Cyclomatic Complexity |
|-------|---------|----------------------|
| Primes.java | Commons-math3-3.2 | 17 |
| Hex.java | Commons-codec | 21 |
| BinaryCodec.java | Commons-codec | 35 |
| CharRange.java | Commons-lang | 45 |
| Range.java | Commons-lang | 57 |
| Fraction.java | Commons-math3-3.2 | 77 |

- [Nguồn: p.3–4 — Sec.4.1, Table 1]

### Metrics
- **Mutation Coverage (MC)** = Mt/M × 100 (tỉ lệ mutants được execute)
- **Mutation Score (MS)** = Mk/Mt × 100 (tỉ lệ mutants bị killed trong số executed)
- **Compilation Success Rate (CSR)** = Tsc/Tst × 100
- Spearman ρ (complexity vs CSR); t-test (MS ChatGPT vs DeepSeek)
- [Nguồn: p.5 — Sec.4.5]

### Kết quả chính — RQ1: Compilation Success Rate (Table 2, p.6)

| CC | Class | ChatGPT CSR | DeepSeek CSR |
|----|-------|-------------|--------------|
| 17 | Primes | **100%** | **100%** |
| 21 | Hex | 80% | 0% |
| 35 | BinaryCodec | 0% | 0% |
| 45 | CharRange | **100%** | 0% |
| 57 | Range | **100%** | **100%** |
| 77 | Fraction | **100%** | **100%** |

- **ChatGPT avg CSR: 63.33%; DeepSeek avg CSR: 50.00%**
- Spearman ρ: ChatGPT = **0.37** (weak positive); DeepSeek = **0.29** (weak positive) → không có mối quan hệ rõ ràng giữa cyclomatic complexity và compilation success
- [Nguồn: p.6 — Table 2, Sec.5.1]

### Kết quả chính — RQ2: Runtime Failures (Tables 3–4, p.7–8)
- 9/30 suites ChatGPT và 11/30 suites DeepSeek compile OK nhưng fail lúc runtime
- ChatGPT failures: invalid cast (byte[] → char[]), comparison failures in negated range, incorrect arithmetic, imprecise numeric conversion
- DeepSeek failures: null comparator, inverted comparison results (8 cases for Range), arithmetic overflow, missing exception handling
- [Nguồn: p.7–8 — Table 3, Table 4, Sec.5.2]

### Kết quả chính — RQ3: Mutation Testing (Table 5, p.8–9)

| CC | Class | Mutants | ChatGPT MC (μ±σ) | ChatGPT MS (μ±σ) | DeepSeek MC (μ±σ) | DeepSeek MS (μ±σ) | Eligible TSs |
|----|-------|---------|-----------------|-----------------|-----------------|-----------------|--------------|
| 17 | Primes | 32 | 76.88%±11.44% | 85.61%±3.49% | **98.44%±1.56%** | **90.47%±0.16%** | ChatGPT 5/5, DeepSeek 2/5 |
| 21 | Hex | 35 | **100%±0%** | **100%±0%** | N/A | N/A | ChatGPT 2/5, DeepSeek 0/5 |
| 35 | BinaryCodec | N/A | N/A | N/A | N/A | N/A | Both 0/5 |
| 45 | CharRange | N/A | N/A | N/A | N/A | N/A | Both 0/5 |
| 57 | Range | 94 | 85.74%±5.62% | 84.24%±2.15% | **96.81%±2.13%** | **86.22%±1.95%** | ChatGPT 5/5, DeepSeek 2/5 |
| 77 | Fraction | 140 | 67.38%±15.18% | 80.63%±2.89% | N/A | N/A | ChatGPT 3/5, DeepSeek 0/5 |

- **DeepSeek đạt MS cao hơn khi eligible**: Primes 90.47% vs ChatGPT 85.61%; Range 86.22% vs ChatGPT 84.24%
- **ChatGPT broader applicability**: eligible suites ở 4/6 classes; DeepSeek chỉ 2/6 classes
- t-test MS toàn bộ: p-value = **0.5** → không significant; nhưng t-test riêng p = **0.04** (DeepSeek higher when comparable)
- Cyclomatic complexity không predict mutation success trực tiếp: high-CC classes (Fraction CC=77, Range CC=57) có thể eligible, nhưng intermediate (BinaryCodec CC=35, CharRange CC=45) fail
- [Nguồn: p.8–9 — Table 5, Sec.5.3]

### Hạn chế
- Chỉ Java; dataset rất nhỏ (6 classes)
- Không compare với SBST baseline (EvoSuite, Pynguin)
- Không detect equivalent mutants → MS values có thể underestimate
- Fully manual execution → scale hạn chế
- Chỉ zero-shot prompting, không thử iterative/few-shot
- [Nguồn: p.10 — Sec.7]

---

## Paper 8 — Huang et al., 2026 — Benchmarking LLMs / ULT (ACM TOSEM)
**Full title:** Benchmarking LLMs for Unit Test Generation from Real-World Functions  
**Authors:** Dong Huang (NUS), Jie M. Zhang (King's College London), Mark Harman (UCL), Qianru Zhang (Cambridge), Mingzhe Du (NUS), See-Kiong Ng (NUS)  
**Venue:** ACM Transactions on Software Engineering and Methodology (ACM TOSEM), 2026  
**DOI:** https://doi.org/10.1145/3805043  
**Artifact:** https://github.com/huangd1999/UnLeakedTestBench

### Tool / Approach
- **Benchmark study**: đánh giá **12 state-of-the-art LLMs** (không propose new LLM)
- **ULT (UnLeakedTestbench)**: benchmark mới, function-level, Python, chống data contamination
- **PLT (PreLeakedTestbench)**: benchmark đối chiếu (leaked tests)
- K-query iterative generation: Round 1 generate test, Rounds 2–K yêu cầu generate test mới khác với các tests đã có
- Inference: greedy decoding, temperature = 0.0, max_tokens = 1024
- Coverage: **line coverage** và **branch coverage** (coverage.py-style)
- Mutation: **Cosmic-Ray** (timeout = 120s/mutant)
- Comparison baseline: **TestEval** (210 LeetCode Python programs)
- Correlation analysis: Pearson (r), Spearman (ρ), Kendall tau (τ) vs BigCodeBench coding performance
- [Nguồn: p.1–9 — Abstract, Sec.3, Sec.4]

### Dataset (ULT)
- **3,909 function-level Python tasks** (ULT) + **18,169 tasks** (PLT)
- Nguồn: **The Stack v2** (large corpus of permissively licensed source code)
- Multi-stage curation:
  1. Cyclomatic complexity ≥ 10 (avg CC = **14.87**, range 10–82)
  2. Self-containment (loại bỏ functions phụ thuộc vào custom external classes)
  3. Testability guarantee (GPT-4o verify ≥ 3 executable test inputs; debug tối đa 3 lần)
  4. Decontamination: loại functions có test cases trong The Stack v2 → tạo ULT; giữ lại làm PLT
- PLT: 18,169 functions (ULT + leaked functions)
- ULT là benchmark duy nhất trong nghiên cứu có all functions CC ≥ 10
- [Nguồn: p.3, p.6–8 — Sec.3.2, Abstract]

### Metrics
- **Pass@k** (accuracy): % test cases generated đúng (syntactically valid + pass assertions)
- **LCov@k**: line coverage (%)
- **BCov@k**: branch coverage (%)
- **Mut@k**: mutation score — % mutants killed (Cosmic-Ray)
- Executability Rate: % tests chạy không RuntimeError (loại assertion errors)
- [Nguồn: p.9 — Sec.3.4]

### 12 LLMs được đánh giá (Table 1, p.10)

| Category | Models |
|----------|--------|
| CodeLlama | CodeLlama-7b-Instruct-hf |
| Seed-Coder | Seed-Coder-8B-Instruct |
| DeepSeekCoder | deepseek-coder-1.3b/6.7b/33b-instruct |
| Gemma-3 | gemma-3-4b/12b/27b-it |
| Qwen2.5-Coder | Qwen2.5-Coder-7B/14B/32B-Instruct |
| Microsoft | Phi-4-mini-instruct |

### Kết quả chính — RQ1.1: Accuracy Pass@k (Table 2, p.12)

| Benchmark | Pass@1 (avg) | Pass@2 (avg) | Pass@5 (avg) |
|-----------|-------------|-------------|-------------|
| **ULT** | **12.69%** | 12.60% | 12.57% |
| PLT | 48.42% | 46.54% | 44.45% |
| TestEval | 57.74% | 55.24% | 51.93% |

- ULT khó hơn đáng kể: Pass@5 chỉ 12.57% so với PLT 44.45% và TestEval 51.93%
- Executability rate ULT: ~**84.75%** (syntactically valid) nhưng accuracy chỉ ~12% → bottleneck là logical reasoning, không phải syntax
- [Nguồn: p.11–12 — Sec.5.1.1, Table 2, Table 3]

### Kết quả chính — RQ1.2: Line Coverage (Table 4, p.13)

| Benchmark | LCov@1 (avg) | LCov@2 (avg) | LCov@5 (avg) |
|-----------|-------------|-------------|-------------|
| **ULT** | **36.22%** | 40.43% | 45.10% |
| PLT | 39.62% | 46.78% | 55.13% |
| TestEval | 87.81% | 90.43% | 92.18% |

- [Nguồn: p.12–13 — Sec.5.1.2, Table 4]

### Kết quả chính — RQ1.3: Branch Coverage (Table 5, p.14)

| Benchmark | BCov@1 (avg) | BCov@2 (avg) | BCov@5 (avg) |
|-----------|-------------|-------------|-------------|
| **ULT** | **17.48%** | 23.36% | 30.22% |
| PLT | 20.20% | 28.88% | 40.07% |
| TestEval | 69.77% | 76.53% | 82.04% |

- ULT: BCov@5 = 30.22%; TestEval: 82.04% → gap lớn do ULT functions có intricate control flows
- [Nguồn: p.13–14 — Sec.5.1.3, Table 5]

### Kết quả chính — RQ1.4: Mutation Score (Table 6, p.14–15)

| Benchmark | Mut@1 (avg) | Mut@2 (avg) | Mut@5 (avg) |
|-----------|------------|------------|------------|
| **ULT** | **20.32%** | 32.12% | **40.21%** |
| PLT | 28.93% | 39.25% | 50.80% |
| TestEval | 40.35% | 45.33% | 49.69% |

- ULT Mut@5 = **40.21%** — thấp hơn cả PLT (50.80%) và TestEval (49.69%)
- [Nguồn: p.14–15 — Sec.5.1.4, Table 6]

### Kết quả chính — RQ2: Cyclomatic Complexity vs Performance (Fig.1, p.16)
- ULT CC range: **10–82**, mean **14.87**; TestEval CC range: 10–40, mean **12.35**
- Trong cùng bin CC [10,20): ULT BCov@5 < 30% nhưng TestEval BCov@5 ~70% → **gap ~40%** dù cùng complexity level
- Trong ULT: correlation âm rõ ràng giữa CC và test performance; e.g., Qwen2.5-Coder-7B: BCov@5 = 42.95% tại CC [10,20) → 2.40% tại CC [80,90)
- [Nguồn: p.14–17 — Sec.5.2, Fig.1]

### Kết quả chính — RQ3: Data Contamination Effect
- PLT consistently outperforms ULT ngay cả khi control cho CC và documentation quality
- Example (Table 8, p.20): Qwen2.5-Coder-32B accuracy CC=11: PLT **70.65%** vs ULT **20.90%** (~50pp gap)
- Correlation ULT vs BigCodeBench: Spearman **ρ = 0.87** (p<0.001); PLT: ρ = 0.57 (p=0.051, không significant)
- → ULT measures genuine reasoning; PLT scores inflated by memorization
- [Nguồn: p.18–21 — Sec.5.3, Table 7, Table 8, Fig.3]

### Hạn chế
- Chỉ Python (Java, C++ không được đánh giá)
- Function-level only, không test integration/system level
- 12 LLMs được chọn; không include GPT-4, Claude, Gemini proprietary trong main evaluation
- Mutation testing chỉ dùng Cosmic-Ray (không PIT)
- "Contamination creep" risk: ULT functions có thể bị included trong future training corpora
- [Nguồn: p.25–27 — Sec.7]

---

## So sánh nhanh 4 papers mới (Papers 5–8)

| Paper | LLM chính | Ngôn ngữ | Dataset size | Branch cov. chính | Mutation score | So sánh với |
|-------|-----------|----------|--------------|-------------------|---------------|-------------|
| ChatGPT Python (Guerino 2025) | GPT-3.5-turbo | Python | 40 programs | LLM ALL 95.9% (decision cov.) | MutPy 91.5% (ALL), Cosmic-Ray 86.9% (ALL) | Pynguin, pre-existing |
| Scenario to Code (Aminata 2025) | Mistral 7B | Java | 70 classes (4 projects, SBST 2020) | 31.3% (2SZSP) vs 49.5% (EvoSuite) | 41.3% (2SZSP) vs 30.8% (EvoSuite) ← LLM WINS | EvoSuite |
| ChatGPT vs DeepSeek (Ferreira/Cabral 2025) | GPT-4o, DeepSeek V3 | Java | 6 classes (Defects4J) | MC: DeepSeek 98.44% (Primes), 96.81% (Range) | MS: DeepSeek 90.47% (Primes), ChatGPT 100% (Hex) | Không có SBST baseline |
| Benchmarking LLMs / ULT (Huang 2026) | 12 LLMs (open-source) | Python | 3,909 functions (ULT) | BCov@5 = 30.22% (ULT avg) | Mut@5 = 40.21% (ULT avg) | TestEval, PLT |

> **Lưu ý quan trọng cho evidence table:**
> - Paper Guerino 2025 dùng *decision coverage* (tương đương branch coverage trong Python)
> - Paper Aminata 2025 là paper DUY NHẤT trong SLR này có mutation score LLM **vượt** EvoSuite (41.3% vs 30.8%), trong khi coverage thấp hơn
> - Paper Ferreira/Cabral 2025 KHÔNG so sánh với EvoSuite hay SBST tool nào
> - Paper Huang 2026 là benchmark study, không propose LLM mới; kết quả thấp hơn papers khác vì benchmark khó hơn (CC ≥ 10, no data leakage)
> - Paper Huang 2026 là paper duy nhất đo tác động của **data contamination** một cách có kiểm soát
