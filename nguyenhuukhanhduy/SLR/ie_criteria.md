# IE Criteria — LLM for Unit Test Case Generation
**Thành viên:** Nguyễn Hữu Khánh Duy
**RQ:** "GPT-4 tự động sinh unit test cases cho Java/Python functions ở cyclomatic complexity trung bình có đạt branch coverage ≥ 80% và mutation score ≥ 60% so với test cases viết thủ công bởi sinh viên không?"
**PICO:** P=Java/Python functions cyclomatic complexity trung bình (11–20) | I=GPT-4 tự động sinh unit test cases | C=unit test cases viết thủ công bởi sinh viên | O=branch coverage ≥ 80% và mutation score ≥ 60%

---

## Inclusion Criteria (IC) — paper PHẢI có đủ tất cả

| Mã | Tiêu chí |
|----|----------|
| **IC-L** | Viết bằng tiếng Anh |
| **IC-Y** | Xuất bản từ 2020 đến nay — Lý do: LLM thế hệ GPT-3+ phổ biến từ 2020; GPT-4 ra mắt 2023, các nghiên cứu trước 2020 không áp dụng LLM thế hệ mới |
| **IC-T** | Đăng trên conference hoặc journal peer-reviewed — không phải blog, thesis, báo cáo kỹ thuật nội bộ, hay preprint chưa review |
| **IC-P** | Về task: sinh unit test case tự động từ source code Java hoặc Python |
| **IC-I** | Dùng kỹ thuật LLM, NLP, hoặc AI-based — cụ thể là GPT, BERT, T5, LLaMA, CodeLlama và tương đương |
| **IC-E** | Có ít nhất 1 con số kết quả định lượng trong Table hoặc Figure của paper gốc — branch coverage, mutation score, line coverage, hoặc tương đương |

## Exclusion Criteria (EC) — loại nếu BẤT KỲ điều kiện nào đúng

| Mã | Tiêu chí |
|----|----------|
| **EC-D** | Trùng lặp với paper đã có trong danh sách (giữ bài mới nhất hoặc đầy đủ nhất) |
| **EC-A** | Không truy cập được full-text (paywalled hoàn toàn, không có preprint hay open access) |
| **EC-S** | Dưới 4 trang — extended abstract, poster, short paper |
| **EC-N** | Không có thực nghiệm gốc — position paper, vision paper, tutorial, secondary study (SLR/survey/mapping study) |
| **EC-O** | Không về task unit test generation: loại nếu paper về (1) test execution hoặc debugging, (2) regression test selection, (3) sinh mutant bằng LLM (không phải sinh unit test), (4) code generation không liên quan test, (5) integration/system test |

---

## Checklist tự kiểm (trước khi bắt đầu screening)

- ☐ Đủ 6 IC (IC-L, IC-Y, IC-T, IC-P, IC-I, IC-E) và 5 EC (EC-D, EC-A, EC-S, EC-N, EC-O)?
- ☐ IC-P là task cụ thể ("sinh unit test case từ source code Java/Python") — không phải "AI trong SE"?
- ☐ IC-I là kỹ thuật cụ thể ("LLM như GPT/BERT/T5/LLaMA") — không phải "công nghệ mới"?
- ☐ EC-O có ≥ 2 task hay bị nhầm? (sinh mutant, test execution, debugging, code gen không liên quan test)
- ☐ IC-Y có lý do chọn năm? (GPT-3+ từ 2020, GPT-4 từ 2023)
