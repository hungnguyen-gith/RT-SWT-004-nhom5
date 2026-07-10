# Gap Statement – LLM for Unit Test Case Generation
**Thành viên:** Nguyễn Hùng (SE180765)
Evidence table: N = 8 papers

---

# Gap Statement – LLM for Unit Test Case Generation

Phát biểu khoảng trống nghiên cứu (Gap Statement) này được tổng hợp và xây dựng 100% dựa trên dữ liệu thực tế trích xuất từ 8 bài báo khoa học hệ thống (N = 8), hoàn toàn loại bỏ các thông tin mang tính chất demo hoặc làm mẫu từ bản nháp cũ. 

---

## 1. CÁC KHOẢNG TRỐNG PHÁT HIỆN TỪ 8 BÀI BÁO HỆ THỐNG (SLR)

### 1.1. GAP-T (Technology - Khoảng trống Công nghệ & Cách tiếp cận)
* **Mô tả:** Phần lớn các nghiên cứu hàng đầu hiện nay tập trung vào các kỹ thuật Prompting nâng cao có cấu trúc phức tạp (như GToT trong Ouédraogo 2024, Method Slicing kết hợp CoT trong HITS 2024, cấu trúc AST traversal trong SymPrompt 2024) hoặc tích hợp các vòng lặp sửa lỗi tự động liên tục (Guerino 2025). Ngược lại, việc đánh giá năng lực "nguyên bản" của GPT-4o mini dưới dạng Zero-shot thuần túy ở cấp độ Class với **dataset kiểm soát CC (5–15)** và so sánh với **Randoop và student-written tests** vẫn chưa được thực hiện. Cabral et al. (2025) có dùng GPT-4o zero-shot ở class level nhưng chỉ trên 6 classes với CC biến thiên 17–77, không kiểm soát dải CC, không so sánh với Randoop, và không có student-written tests làm ground truth.
* **Bằng chứng thực nghiệm từ 8 Papers:**
  * **HITS (2024):** Bắt buộc phải dựa vào cơ chế rã nhỏ hàm (Method Slicing) + CoT + Self-debug trên nền GPT-3.5 để đạt hiệu quả cao.
  * **SymPrompt (2024):** Dựa trên CodeGen2 16B kết hợp trích xuất ràng buộc tĩnh qua AST (TreeSitter parsing framework).
  * **Tang et al. (2024):** Dù so sánh trực tiếp với công cụ SBST (EvoSuite) nhưng lại sử dụng phiên bản ChatGPT cũ (bản cố định ngày 30/01/2023).

### 1.2. GAP-M (Metric - Khoảng trống Thước đo đánh giá)
* **Mô tả:** Có sự bất đối xứng lớn về mặt metric đánh giá giữa các nghiên cứu. Mặc dù Mutation Score (Điểm số kiểm thử đột biến) được công nhận là thước đo chuẩn xác nhất để đánh giá chất lượng thực tế của test suite (khả năng phát hiện lỗi logic tiềm ẩn), phần lớn các nghiên cứu lớn (như HITS 2024, Tang 2024, Ouédraogo 2024, SymPrompt 2024) vẫn chỉ dừng lại ở việc báo cáo độ bao phủ mã nguồn thông thường (Line/Branch Coverage). Đặc biệt, trong hệ sinh thái Python, việc đánh giá song song cả Branch Coverage và Mutation Score sử dụng các bộ tool tiêu chuẩn (như Coverage.py phối hợp với MutPy/Cosmic-Ray) là vô cùng hiếm hoi và thường chỉ được thực hiện trên các tệp mã nguồn có quy mô rất nhỏ.
* **Bằng chứng thực nghiệm từ 8 Papers:**
  * **HITS (2024), Tang (2024), Ouédraogo (2024), SymPrompt (2024):** Hoàn toàn bỏ trống (không báo cáo) metric Mutation Score.
  * **Aminata et al. (2025):** Báo cáo Mutation Score vượt trội so với EvoSuite (41.3% vs 30.8%), nhưng lại gặp phải tỷ lệ lỗi biên dịch (Compilation Failure Rate) cực kỳ nặng nề lên đến 64% test suite sinh ra không thể thực thi.
  * **Cabral et al. (2025):** So sánh GPT-4o và DeepSeek V3 về Mutation Score bằng công cụ PIT nhưng hoàn toàn không có đối chứng (baseline) với các công cụ kiểm thử dựa trên tìm kiếm (SBST) như EvoSuite.

### 1.3. GAP-D (Dataset & Experimental Control - Khoảng trống Tập dữ liệu & Kiểm soát thực nghiệm)
* **Mô tả:** Đây là khoảng trống nghiêm trọng nhất. Các nghiên cứu hiện tại phân tách thành hai thái cực: Một bên sử dụng các dataset dự án thế giới thực (như Defects4J, SF110, Apache Commons) làm mốc đánh giá nhưng lại vướng vào hiện tượng *Data Contamination* (Rò rỉ dữ liệu) — tức LLM đã được học thuộc lòng các đoạn code này trong quá trình huấn luyện, dẫn đến kết quả độ bao phủ bị phóng đại. Thái cực còn lại cố gắng xây dựng benchmark chống rò rỉ (như bộ ULT trong Huang 2026) thì lại chỉ đánh giá ở cấp độ Function-level (Hàm đơn lẻ), hoàn toàn bỏ qua cấu trúc Class-level (bao gồm các trạng thái hướng đối tượng, hàm dựng, và các dependency nội bộ). Thêm vào đó, chưa có nghiên cứu nào thực hiện việc phân tầng (stratify) và kiểm soát chặt chẽ Cyclomatic Complexity (Độ phức tạp vòng mạch) trong khoảng kiểm soát cụ thể (ví dụ: CC từ 5 đến 15) như một biến độc lập ảnh hưởng đến cả hai ngôn ngữ Java và Python song song trong cùng một điều kiện thực nghiệm.
* **Bằng chứng thực nghiệm từ 8 Papers:**
  * **Huang et al. (2026):** Cấu hình ngưỡng CC ≥ 10 nhằm kiểm soát độ phức tạp vòng mạch, tuy nhiên chỉ giới hạn ở Function-level trên Python và chưa đánh giá cấp Class. Chứng minh rò rỉ dữ liệu làm sai lệch kết quả (Pass@5 của ULT là 12.57% so với bộ rò rỉ PLT là 44.45%).
  * **Guerino & Vincenzi (2025):** Thử nghiệm trên Python nhưng tập dữ liệu cực kỳ nhỏ, chỉ mang tính chất minh họa thuật toán cơ bản với độ dài trung bình vỏn vẹn 32.2 SLOC (cấu trúc dữ liệu & thuật toán quy mô nhỏ), không kiểm soát CC như một biến độc lập.
  * **Cabral et al. (2025):** Khảo sát cấp Class-level của Java với CC biến thiên rộng (17-77) nhưng kích thước mẫu quá bé (chỉ có đúng 6 classes từ Defects4J).

---

## 2. PHÁT BIỂU GAP TỔNG HỢP (SYNTHESIS GAP STATEMENT)

> **"Các nghiên cứu thực nghiệm hiện tại về LLM-based unit test generation đang bị giới hạn bởi hiện tượng rò rỉ dữ liệu (data contamination) trên các kho mã nguồn mở phổ biến ở cấp độ Class-level, hoặc chỉ tập trung đánh giá các hàm đơn lẻ (Function-level) mà thiếu đi sự kiểm soát phân tầng chặt chẽ đối với độ phức tạp vòng mạch (Cyclomatic Complexity) từ mức trung bình đến khó (CC 5–15) như một biến độc lập. Đồng thời, chưa có một nghiên cứu đa ngôn ngữ (Java và Python) nào đánh giá năng lực Zero-shot thuần túy của GPT-4o mini ở cấp độ Class nhằm thiết lập một đường cơ sở (baseline) chuẩn hóa, đáp ứng đồng thời cả tiêu chí kiểm thử nghiêm ngặt bao gồm Branch Coverage ổn định và điểm số đột biến (Mutation Score) cao mà không làm đánh đổi tỷ lệ biên dịch thành công (Compilation Success Rate)."**