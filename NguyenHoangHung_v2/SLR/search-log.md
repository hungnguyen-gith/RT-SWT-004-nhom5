# Search Log – LLM for Unit Test Case Generation
**Thành viên:** Nguyễn Hùng (SE180765)
**Ngày thực hiện:** 2026-06-07

---

## Chuỗi tìm kiếm

### String A
**Query:**
("large language model" OR "LLM" OR "GPT-4" OR "ChatGPT") AND ("unit test" OR "test case generation" OR "automated testing") AND ("Java" OR "Python") AND ("branch coverage" OR "mutation score" OR "code coverage")

**Database:** IEEE Xplore
**Bộ lọc:** Year 2020–2026, English only, Conference + Journal
**Ngày search:** 2026-06-07
**Số kết quả:** 20

---

### String B
**Query:**
("GPT-4" OR "large language model" OR "LLM") AND ("unit test generation" OR "test case generation" OR "automated unit testing") AND ("cyclomatic complexity" OR "branch coverage" OR "mutation testing")

**Database:** ACM Digital Library
**Bộ lọc:** Year 2020–2026, English only
**Ngày search:** 2026-06-07
**Số kết quả:** 208

---

### String C
**Query:**
("large language model" OR "GPT" OR "LLM") AND ("unit test" OR "test generation") AND ("Java" OR "Python") AND ("coverage" OR "mutation score")

**Database:** Semantic Scholar
**Bộ lọc:** Manual filter sau (IC-Y: 2020+)
**Ngày search:** 2026-06-07
**Số kết quả:** 40

---

### String D
**Query:**
LLM "unit test generation" "branch coverage" OR "mutation score" Java Python

**Database:** Google Scholar
**Bộ lọc:** Custom range 2020–2026, loại patent và citation
**Ngày search:** 2026-06-07
**Số kết quả:** 347

---

### String E
**Query:**
("large language model" OR "GPT-4" OR "LLM") AND ("unit test" OR "test case generation") AND ("Java" OR "Python")

**Database:** OpenAlex
**Bộ lọc:** publication_year: 2020–2026, type: journal-article | conference-paper
**Ngày search:** 2026-06-07
**Số kết quả:** 152

---

## Tổng hợp trước dedup

| Database | String | Kết quả |
|----------|--------|---------|
| IEEE Xplore | String A | 20 |
| ACM Digital Library | String B | 208 |
| Semantic Scholar | String C | 40 |
| Google Scholar | String D | 347 |
| OpenAlex | String E | 152 |
| Snowballing (CrossRef) | Phần S | 0 |
| **Tổng trước dedup** | | **767** |
| **Sau dedup** | | **62** |

---

## Phần S – Cross-reference Search (Snowballing)

**Phương pháp:** Backward snowballing — đọc reference list của các paper pass V2 screen.
**Công cụ:** CrossRef (crossref.org) để lookup DOI/metadata; Google Scholar để check full-text.
**Ngày thực hiện:** Chưa thực hiện — thực hiện sau khi hoàn thành V2 screening.
**Paper included đã scan:** 0
**Paper mới phát hiện:** 0
