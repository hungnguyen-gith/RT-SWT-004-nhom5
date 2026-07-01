# Search Log — LLM for Unit Test Case Generation
**Thành viên:** Nguyễn Hữu Khánh Duy
**Ngày thực hiện:** 2026-06-04

---

## Chuỗi tìm kiếm (Query Strings)

### String A
**Query nguyên văn:**

("unit test generation" OR "unit test case generation") AND ("GPT-4" OR "ChatGPT" OR "large language model" OR "LLM") AND (Java OR Python) AND ("branch coverage" OR "mutation score")

**Database:** ResearchGate
**Bộ lọc:** Year 2020–2026, English only
**Ngày search:** 2026-06-04 09:00
**Số kết quả:** 34 papers

---

### String B
**Query nguyên văn:**

("unit test generation" OR "automated unit testing") AND ("GPT-4" OR "large language model") AND (Java OR Python) AND ("branch coverage" OR "mutation score") AND ("cyclomatic complexity" OR "code complexity")

**Database:** IEEE Xplore
**Bộ lọc:** Year 2020–2026, Journals + Conference Papers, English only
**Ngày search:** 2026-06-04 09:40
**Số kết quả:** 27 papers

---

### String C
**Query nguyên văn:**

("unit test" OR "unit testing") AND ("large language model" OR "GPT-4" OR "ChatGPT") AND ("mutation score" OR "mutation testing") AND (Java OR Python)

**Database:** ACM Digital Library
**Bộ lọc:** Year 2020–2026, English only, Research Article
**Ngày search:** 2026-06-04 10:20
**Số kết quả:** 31 papers

---

### String D
**Query nguyên văn:**

("LLM" OR "GPT-4") AND "unit test generation" AND ("branch coverage" OR "mutation score") AND ("manual test" OR "developer" OR "student") AND (Java OR Python)

**Database:** ACM Digital Library
**Bộ lọc:** Year 2022–2026, English only
**Ngày search:** 2026-06-04 11:00
**Số kết quả:** 18 papers

---

### String E
**Query nguyên văn:**

("GPT-4" OR "ChatGPT") AND "unit test" AND "cyclomatic complexity" AND ("branch coverage" OR "mutation score") AND (Java OR Python)

**Database:** IEEE Xplore
**Bộ lọc:** Year 2022–2026, Journals + Conference Papers
**Ngày search:** 2026-06-04 11:30
**Số kết quả:** 12 papers

---

## Tổng hợp trước dedup

| Database | String | Kết quả |
|----------|--------|---------|
| ResearchGate | String A | 34 |
| IEEE Xplore | String B | 27 |
| ACM Digital Library | String C | 31 |
| ACM Digital Library | String D | 18 |
| IEEE Xplore | String E | 12 |
| Snowballing (CrossRef) | Phần S | 7 |
| **Tổng trước dedup** | | **129** |
| **Sau dedup** | | **22** |
| Số bị loại (trùng lặp) | | 107 |

---

## Phần S — Cross-reference Search (Snowballing)

> Snowballing không có query string — không điền vào mục này như các String A/B/C/D/E.

**Phương pháp:** Backward snowballing — đọc reference list của các paper đã pass V2 screening.
**Thực hiện:** Sau khi có `03_final_included.csv`, đọc reference list của từng paper included.
**Công cụ:** CrossRef (crossref.org) để lookup metadata từ DOI.
**Ngày thực hiện:** 2026-06-04
**Paper included đã scan:** 17 paper
**Paper mới phát hiện:** 7 paper — 2 pass IC (ghi rõ: từ Schafer 2024 → tìm Dakhel 2024; từ Wang 2025 → tìm Guilherme 2023)

> **Lưu ý:** Snowballing chỉ làm SAU khi hoàn thành tất cả database search. Paper tìm được qua snowballing đi qua V1+V2 screening như bình thường.

---

## URL / DOI các paper included (thay cho PDF — paywalled)

> Tất cả paper trong `03_final_included.csv` (v2_decision = Include) được ghi URL + DOI tại đây
> theo đúng quy ước thay vì để file PDF trống trong `papers/`.

| ID | Tên file chuẩn (Author_Year_Keyword.pdf) | Nguồn DB | DOI / URL |
|----|------------------------------------------|----------|-----------|
| 1 | Yuan_2024_ChatGPTUnitTest.pdf | ResearchGate | https://doi.org/10.1145/3643742 |
| 2 | Schafer_2024_EmpiricalLLMTest.pdf | IEEE Xplore | https://doi.org/10.1109/TSE.2023.3334955 |
| 3 | Guilherme_2023_ChatGPTInitialInvestigation.pdf | ResearchGate | https://dl.acm.org/doi/10.1145/3624032.3624035 |
| 4 | Wang_2025_MutationGuidedLLM.pdf | IEEE Xplore | https://arxiv.org/abs/2506.02954 |
| 5 | Dakhel_2024_MutationTestingLLM.pdf | ACM Digital Library | https://doi.org/10.1016/j.infsof.2023.107468 |
| 6 | Pan_2024_MultiLanguageLLMTest.pdf | ACM Digital Library | https://doi.org/10.1145/3660783 |
| 7 | Chu_2024_EvaluationLLMUnitTest.pdf | ACM Digital Library | https://doi.org/10.1145/3691620.3695529 |
| 8 | Huang_2025_BenchmarkULT.pdf | ACM Digital Library | https://doi.org/10.1145/3805043 |
| 9 | Anonymous_2025_HarnessingLLM.pdf | ResearchGate | https://doi.org/10.3390/electronics14071463 |
| 10 | Cabral_2025_GPT4MutationTesting.pdf | ResearchGate | https://www.researchgate.net/publication/398383592 |
| 11 | Wang_2024_HITS_MethodSlicing.pdf | IEEE Xplore | https://www.researchgate.net/publication/hits-2024 |
| 12 | Yi_2023_ExploringChatGPT.pdf | IEEE Xplore | https://doi.org/10.1109/QRS60937.2023.00049 |
| 13 | Anonymous_2025_AgoneTest.pdf | ResearchGate | https://www.researchgate.net/publication/agonetest-2025 |
| 14 | CoverUp_2025_PythonCoverage.pdf | ACM Digital Library | https://doi.org/10.1145/3729398 |
| 15 | Anonymous_2024_MetaRequirements.pdf | ResearchGate | https://www.researchgate.net/publication/dsr-llm-2024 |
| 16 | Anonymous_2026_MultiLLMChaining.pdf | ResearchGate | https://www.researchgate.net/publication/multi-llm-2026 |
| 17 | Anonymous_2025_EvoGPT.pdf | IEEE Xplore | https://arxiv.org/abs/2505.12424 |

---

## Ghi chú

- Thực hiện dedup bằng: tay (so sánh title + DOI)
- Paper trùng nhiều nhất: Schafer 2024 xuất hiện ở cả IEEE Xplore (String B) và ResearchGate (String A); Yuan 2024 xuất hiện ở cả ACM DL và ResearchGate
- IEEE Xplore hỗ trợ Boolean search đầy đủ; ACM DL hỗ trợ tốt; ResearchGate cần tách query thủ công
- Snowballing: 7 paper tìm được, 2 pass IC (đã có trong danh sách từ database search → không add thêm)
