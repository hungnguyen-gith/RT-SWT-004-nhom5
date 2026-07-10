# Tổng hợp thông tin từ 4 PDF — Phục vụ Evidence Table
> Mỗi mục ghi rõ: nguồn (tên paper + trang PDF)

---

## Paper 1 — Wang et al., 2024 — HITS (ASE '24)
**Full title:** HITS: High-coverage LLM-based Unit Test Generation via Method Slicing  
**Authors:** Zejun Wang, Kaibo Liu, Ge Li, Zhi Jin (Peking University)  
**Venue:** 39th IEEE/ACM ASE, Oct–Nov 2024  
**DOI:** https://doi.org/10.1145/3691620.3695501

### Tool / Approach
- **HITS** = LLM (GPT-3.5-turbo-0125) + method slicing (divide-and-conquer)
- Focal method decomposed thành các **code slices** theo "problem-solving steps"
- Dùng **Chain-of-Thought** để hướng dẫn LLM decompose + generate test từng slice
- Có bước **self-debug** (LLM tự fix broken tests dựa trên JVM error report)
- Framework: JUnit 5, Mockito; coverage đo bằng **JaCoCo**
- [Nguồn: p.1258–1260 — Abstract, Sec.1, Sec.3]

### Dataset
- **10 Java open-source projects** thu thập từ Internet, tập trung vào **complex methods** (cyclomatic complexity > 10)
- Projects gồm: Commons-CLI, Commons-CSV, Gson, Commons-codec, Commons-collections4, JDom2 (LLM đã học), Datafaker, Event-ruler, windward, batch-processing-gateway (LLM chưa học)
- Tổng: **114 complex methods** (MUTs)
- [Nguồn: p.1261–1262 — Table 2, Sec.4.1]

### Metrics
- **Line coverage** và **branch coverage** (đo bằng JaCoCo)
- Pass rate (tỉ lệ test executable)
- So sánh vs. baselines: ChatUniTest, ChatTester, SymPrompt, EvoSuite
- [Nguồn: p.1262 — Sec.4.1]

### Kết quả chính
| Phương pháp | Avg. Line Cov. | Avg. Branch Cov. |
|-------------|---------------|-----------------|
| **HITS**    | **55.09%**    | **48.12%**      |
| EvoSuite    | 39.10%        | 38.46%          |
| ChatUniTest | 32.48%        | 27.07%          |
| ChatTester  | 20.71%        | 18.20%          |
| SymPrompt   | 26.32%        | 25.10%          |

- HITS outperforms tất cả baselines (LLM + SBST) trên **complex methods**
- Khi LLM đã học project (training set), slicing đôi khi không vượt ChatUniTest (vì LLM "recall" tốt hơn)
- Pass rate của HITS: **69.11%** avg vs. ChatUniTest 41.82%, ChatTester 16.10%, SymPrompt 21.00%
- Wilcoxon test: HITS significantly outperforms trong **75% cases**, p < 0.05
- [Nguồn: p.1263–1264 — Table 4, Table 5, Table 6, Sec.4.2–4.3]

### Hạn chế
- Chỉ Java; chỉ dùng GPT-3.5-turbo (budget hạn chế, không test GPT-4)
- Dataset nhỏ (tối đa 30 complex methods/project) do budget hạn chế
- Mutation score không được báo cáo
- Slicing đôi khi không cải thiện với projects LLM đã học rất kỹ
- [Nguồn: p.1265–1266 — Sec.5.4]

---

## Paper 2 — Tang et al., 2024 — ChatGPT vs SBST (IEEE TSE)
**Full title:** ChatGPT vs SBST: A Comparative Assessment of Unit Test Suite Generation  
**Authors:** Yutian Tang, Zhijie Liu, Zhichao Zhou, Xiapu Luo  
**Venue:** IEEE Transactions on Software Engineering (published as arXiv:2307.00588v1, Jul 2023 → IEEE TSE 2024)  
**Artifact:** https://sites.google.com/view/chatgpt-sbst

### Tool / Approach
- **ChatGPT** (GPT-3, phiên bản Jan 30 2023) vs **EvoSuite** (SBST)
- Prompt: *"Write a JUnit test case to cover methods in the following code (one test case for each method): ${input}?"*
- EvoSuite chạy **30 lần/class** (default settings) để giảm randomness bias
- Giới hạn input: lớp > 4,096 tokens bị loại bỏ
- Coverage đo bằng **JaCoCo** (statement coverage / instruction coverage)
- Bug detection dùng **Defects4J** benchmark (835 bugs, 17 projects)
- Code style check: **Checkstyle** (Google Style + SUN Style)
- Bug scan: **SpotBugs** (static analysis)
- Complexity: **PMD** (cognitive + cyclomatic)
- [Nguồn: p.1–3 — Sec.1, Sec.3]

### Dataset
- **RQ1–3:** 207 Java classes từ 75 projects (từ DynaMOSA benchmark ban đầu 346 classes/117 projects, loại classes > 4096 tokens và projects không build được)
- **RQ4 (bug detection):** Defects4J — 212 exception-related bugs từ 16 projects (Chart, Cli, Closure, Codec, Collections, Compress, Csv, Gson, JacksonCore, JacksonDatabind, JacksonXml, Jsoup, JxPath, Lang, Math, Time)
- [Nguồn: p.2–3 — Sec.3.1, Sec.3.3]

### Metrics
- **Statement coverage (SC)** — dùng JaCoCo instruction coverage
- **Bug detection** — số lượng exception bugs detect được
- Correctness (compile rate), readability (code style violations, cognitive/cyclomatic complexity)
- Vargha-Delaney Â measure để so sánh thống kê
- [Nguồn: p.6–8 — Sec.4.3, Sec.4.4]

### Kết quả chính — Statement Coverage (RQ3)
| Phương pháp | Avg. SC (all projects) |
|-------------|----------------------|
| EvoSuite (max) | 77.4% |
| EvoSuite (avg) | 74.2% (= 74.5% per table) |
| **ChatGPT**    | **55.4%** |

- EvoSuite outperforms ChatGPT **19.1%** (statement coverage)
- ChatGPT outperforms EvoSuite chỉ ở **37/207 classes (17.87%)** và **10/75 projects (13.33%)**
- Vargha-Delaney overall: **0.71 (medium)** — EvoSuite áp đảo
- [Nguồn: p.6–8 — Table 8, Table 9, Table 10, Sec.4.3]

### Kết quả chính — Correctness (RQ1)
- ChatGPT generate thành công **207/207 classes**
- **69.6% (144/207)** compile & execute không cần can thiệp thủ công
- **60 test cases** fix được với IDE; **3 test cases** không fix được nếu không có domain knowledge
- SpotBugs: **61.2%** test cases bug-free; chỉ **9.8%** ở mức Scariest/Scary
- [Nguồn: p.3–4 — Sec.4.1]

### Kết quả chính — Readability (RQ2)
- Cognitive complexity: **100% methods** ở mức Low (<5) → dễ đọc
- Cyclomatic complexity: **3300/3302 methods** ở mức Low (1–4)
- [Nguồn: p.5–6 — Table 6, Table 7, Sec.4.2]

### Kết quả chính — Bug Detection (RQ4)
| Phương pháp | Bugs detected (trong 212 exception bugs) | Avg. SC |
|-------------|------------------------------------------|---------|
| ChatGPT     | **44 (21%)**                             | 50%     |
| EvoSuite    | **55 (26%)**                             | 67%     |

- ChatGPT detect bugs trong Chart, Compress, Lang tốt hơn EvoSuite (theo số lượng)
- Assertions của ChatGPT đôi khi không đáng tin cậy (logic bugs) → chỉ focus vào exception bugs
- [Nguồn: p.9 — Table 13, Sec.4.4]

### Hạn chế
- Chỉ Java; GPT-3 (không phải GPT-4) — phiên bản cố định Jan 30 2023
- Closed-source model, không biết training data
- Mutation score không được báo cáo
- Chỉ exception-related bugs trong Defects4J được đánh giá (không đánh giá logic bugs)
- [Nguồn: p.9–10 — Sec.5]

---

## Paper 3 — Ouédraogo et al., 2024 — LLMs and Prompting (ASE '24)
**Full title:** LLMs and Prompting for Unit Test Generation: A Large-Scale Evaluation  
**Authors:** Ouédraogo, Kaboré, Song, Klein (Univ. Luxembourg), Tian (Univ. Melbourne), Koyuncu (Bilkent Univ.), Lo (SMU), Bissyandé (Univ. Luxembourg)  
**Venue:** 39th IEEE/ACM ASE '24, Oct–Nov 2024  
**DOI:** https://doi.org/10.1145/3691620.3695330

### Tool / Approach
- **4 LLMs:** GPT-3.5, GPT-4, Mistral 7B, Mixtral 8x7B
- **5 prompting techniques:** Zero-shot (ZSL), Few-shot (FSL), Chain-of-Thought (CoT), Tree-of-Thoughts (ToT), Guided Tree-of-Thoughts (**GToT** — hybrid CoT+ToT)
- Mỗi experiment lặp lại **30 lần** để giảm randomness
- Tools: EvoSuite (DynaMOSA), SpotBugs, JaCoCo, Checkstyle, PMD, Javalang
- [Nguồn: p.2464–2465 — Sec.1, Sec.2.2, Sec.3.1]

### Dataset
- **3 datasets:**
  1. **SF110** — 110 Java projects benchmark (EvoSuite benchmark chuẩn)
  2. **Defects4J** — real-world bugs từ open-source Java projects
  3. **Custom Mini Dataset (CMD)** — Java classes từ OceanBase Developer Center (ODC) và Conductor OSS
- Tổng: **216,300 tests** được generate cho **690 Java classes**
- [Nguồn: p.2464 — Sec.2.2]

### Metrics
- Correctness & compilability, readability (code style, complexity)
- **Line coverage, method coverage** (JaCoCo)
- Bug detection (Defects4J)
- [Nguồn: p.2465 — Sec.3.1]

### Kết quả chính
**RQ1 (Correctness & compilability):**
- GToT prompting → highest correct + compilable test rate
- ZSL → lowest
- Structured prompts consistently improve correctness across all LLMs

**RQ2 (Code Coverage):**
- EvoSuite typically achieves **higher line and method coverage**
- LLMs with **CoT và GToT** matched or **exceeded EvoSuite's coverage** in some cases, especially on the **Custom Mini Dataset**

**RQ3 (Bug Detection):**
- On Defects4J: CoT và GToT prompts detect nhiều bugs, **occasionally surpassing EvoSuite**
- Detection rates lower on CMD → LLMs struggle với complex/unfamiliar code
- [Nguồn: p.2465 — Sec.3.2]

> ⚠️ **Lưu ý:** Paper này là 2-page short paper (ASE '24 tool/industry track). Không có bảng số liệu chi tiết (coverage %, bug count) trong phần được cung cấp — chỉ có kết quả định tính. Nếu cần số liệu cụ thể, cần xem full paper/artifact.

### Hạn chế
- Chỉ Java; LLMs cần cải thiện về correctness
- Performance thấp hơn trên complex/unfamiliar codebases (CMD)
- Không báo mutation score
- [Nguồn: p.2465 — Sec.4]

---

## Paper 4 — Ryan et al., 2024 — Code-Aware Prompting / SymPrompt (ACM SE)
**Full title:** Code-Aware Prompting: A Study of Coverage-Guided Test Generation in Regression Setting using LLM  
**Authors:** Gabriel Ryan (Columbia Univ.), Siddhartha Jain, Mingyue Shang, Shiqi Wang, Xiaofei Ma, Murali Krishna Ramanathan, Baishakhi Ray (AWS AI Labs)  
**Venue:** Proc. ACM Softw. Eng. 1, FSE, Article 43 (July 2024)  
**DOI:** https://doi.org/10.1145/3643769

### Tool / Approach
- **SymPrompt** = code-aware, path-constraint prompting strategy cho LLMs
- 3 bước: (i) thu thập **approximate path constraints** qua static AST traversal, (ii) xây **type + dependency context**, (iii) generate tests per-path iteratively
- Dùng **TreeSitter** parsing framework (Python)
- Không cần fine-tuning; hoạt động với pretrained LLMs
- Baseline LLM chính: **CodeGen2 16B** (open-source); cũng evaluate **GPT-4**
- Framework: Python (pytest/unittest), coverage đo bằng coverage.py-style
- [Nguồn: p.43:1–43:6 — Abstract, Sec.1, Sec.3]

### Dataset
- **897 focal methods** từ **26 open-source Python projects**
- Chọn methods mà **Pynguin** (SBST tool for Python) **không đạt full coverage** trong 10 runs → đây là challenging methods
- Pynguin baseline: avg **72.4% line coverage, 64% branch coverage** trên dataset này
- Subset "Unseen Projects" (3 projects không có trong CodeGen2 training data) để kiểm tra memorization
- [Nguồn: p.43:11 — Sec.4, Benchmark Programs]

### Metrics
- Pass@1, FM Call@1, Correct@1
- **Line coverage và branch coverage** (avg trên focal method)
- [Nguồn: p.43:11 — Evaluation Metrics]

### Kết quả chính — RQ1: Full Benchmark (CodeGen2)

| Phương pháp | Pass@1 | Correct@1 | Line Cov. | Branch Cov. |
|-------------|--------|-----------|-----------|-------------|
| No-Op Tests | 1.00 | 0.00 | 0.33 | 0.33 |
| Baseline Prompt | 0.12 | 0.03 | 0.38 | 0.40 |
| **SymPrompt** | **0.41** | **0.15** | **0.48** | **0.44** |
| Pynguin (SBST) | — | — | 0.72 | 0.64 |
| SymPrompt Filtered | 0.81 | 0.81 | 0.77 | 0.66 |

- SymPrompt: **5× more correct generations** vs baseline prompt
- SymPrompt: **+10% line coverage, +4% branch coverage** vs baseline prompt
- **SymPrompt Filtered** (bỏ test suites hoàn toàn fail): line 77% vs Pynguin 72%, branch 66% vs Pynguin 64%
- [Nguồn: p.43:12–43:13 — Table 1, Sec.4.1]

### Kết quả chính — RQ4: GPT-4

| Phương pháp | Correct@1 | Line Cov. | Branch Cov. |
|-------------|-----------|-----------|-------------|
| Baseline Prompt | 0.09 | 0.36 | 0.40 |
| **SymPrompt (GPT-4)** | **0.25** | **0.74** | **0.74** |

- SymPrompt với GPT-4: cải thiện coverage **>2× (105% relative)** so với baseline prompting
- Calling context đặc biệt quan trọng với GPT-4 (giảm hallucinated imports)
- [Nguồn: p.43:15–43:16 — Table 2 RHS, Sec.4.4]

### Kết quả chính — RQ3: Ablation (CodeGen2, 100 sampled)

| Phương pháp | Correct@1 | Line Cov. | Branch Cov. |
|-------------|-----------|-----------|-------------|
| Baseline Prompt | 0.04 | 0.30 | 0.29 |
| Constraints Only | 0.17 | 0.49 | 0.38 |
| Context Only | 0.06 | 0.42 | 0.35 |
| **SymPrompt (full)** | **0.26** | **0.53** | **0.42** |

- Path constraint prompts đóng góp nhiều hơn calling context
- [Nguồn: p.43:15 — Table 2 LHS, Sec.4.3]

### Hạn chế
- Chỉ **Python** (không Java); dùng CodeGen2 (không phải GPT-4 làm baseline chính)
- Mutation score không được báo cáo
- Pynguin vẫn đạt coverage cao hơn SymPrompt (CodeGen2) trước khi filter
- Chỉ regression setting (không test bug-finding ability)
- Không evaluate trên Java → khó so sánh trực tiếp với các paper khác trong SLR
- [Nguồn: p.43:16 — Sec.5]

---

## So sánh nhanh 4 papers

| Paper | LLM chính | Ngôn ngữ | Dataset size | Branch cov. chính | Mutation score | So sánh với |
|-------|-----------|----------|--------------|-------------------|---------------|-------------|
| HITS (Wang 2024) | GPT-3.5 | Java | 114 complex methods | 48.12% (HITS avg) | ❌ | EvoSuite, ChatUniTest, SymPrompt |
| ChatGPT vs SBST (Tang 2024) | GPT-3 | Java | 207 classes | SC 55.4% (ChatGPT) | ❌ | EvoSuite |
| LLMs & Prompting (Ouédraogo 2024) | GPT-3.5/4, Mistral | Java | 690 classes, 216,300 tests | Không có số cụ thể | ❌ | EvoSuite |
| SymPrompt (Ryan 2024) | CodeGen2, GPT-4 | Python | 897 methods | 44% (SymPrompt) / 64% (Pynguin) | ❌ | Pynguin (SBST) |

> **Lưu ý quan trọng cho evidence table:**  
> - Paper Tang 2024 dùng *statement coverage* (không phải branch coverage) làm metric chính  
> - Paper Ouédraogo 2024 không cung cấp số liệu định lượng cụ thể trong bản 2-page này  
> - Tất cả 4 papers **không báo mutation score**  
> - Ryan 2024 là paper duy nhất dùng Python (các paper còn lại đều Java)
