Gap Statement — LLM for Unit Test Case Generation

Thành viên: Nguyễn Hữu Khánh Duy
Evidence table: N = 20 paper


GAP-T (Technology): GPT-4 chưa được so sánh trực tiếp với sinh viên viết tay

Bằng chứng: Cột Tool/LLM và "So sánh" trong evidence table — paper #1 (Yuan 2024) so với 5 Java developers;
 paper #6 (Pan 2024, ASTER) so với developer-written tests, kết quả cho thấy test do ASTER sinh ra tự nhiên hơn cả test do developer viết, nhưng vẫn là developer;
 paper #13 (AgoneTest) so với "human-written" nhưng không xác định rõ là developer hay sinh viên;
  paper #7 (Foster 2025, Meta) so với senior engineers. Không paper nào trong 20 paper dùng sinh viên đại học (1–2 năm kinh nghiệm) làm nhóm so sánh C.

GAP-M (Metric): Chưa có paper nào đo đồng thời branch coverage VÀ mutation score trên cùng bộ Java/Python medium CC functions

Bằng chứng: Cột Metric trong evidence table — paper #9 (MDPI 2025) đo branch 97.16% nhưng không đo mutation;
 paper #10 (Cabral 2025) đo mutation 85.61% (Primes, medium CC) nhưng không báo cáo branch riêng;
  paper #5 (Wang et al. 2025) cảnh báo quan trọng: một số test suite đạt 100% coverage nhưng chỉ 4% mutation score — cho thấy hai metrics không thể thay thế nhau, nhưng paper này cũng không kiểm soát CC level khi đo. Một nghiên cứu khác (#21, ResearchGate 2025) báo cáo chain-of-thought đạt tới 96.3% branch coverage và mutation score trung bình 57% — gần đạt threshold nhưng không kiểm soát CC = 11–20 và không so với sinh viên.

GAP-D (Dataset): Không có benchmark Python ở cyclomatic complexity TRUNG BÌNH (11–20) với mutation testing đầy đủ

Bằng chứng: Cột Dataset trong evidence table — paper #8 (Huang 2025, ULT) là benchmark Python duy nhất có đủ branch + mutation nhưng được thiết kế với high CC;
 paper #14 (CoverUp 2025) đạt 80% branch coverage Python nhưng không đo mutation score và không kiểm soát CC level;
  paper #10 (Cabral 2025) có medium CC + mutation nhưng là Java, không phải Python. Không paper nào dùng Python dataset với CC = 11–20 làm tiêu chí chọn hàm.


Phát biểu GAP tổng hợp

Từ 20 paper trong evidence table (ResearchGate, IEEE Xplore, ACM Digital Library), bằng chứng cho thấy GPT-4/GPT-4o có thể đạt branch coverage ≥ 80% (Java, #9: 97.16%; #21: 96.3%) và mutation score ≥ 60% trong một số điều kiện riêng lẻ (Java medium CC, #10: 85.61%), nhưng các kết quả này không đồng nhất — paper #16 (Seed&Steer) chỉ đạt branch ~73%, và paper #5 cho thấy branch cao không đảm bảo mutation cao (100% vs 4%). Quan trọng hơn, chưa có nghiên cứu nào: (1) so sánh trực tiếp GPT-4 với sinh viên (không phải developer hay senior engineer) làm nhóm C, (2) đo đồng thời cả hai ngưỡng (branch ≥ 80% và mutation ≥ 60%) trên cùng bộ Java/Python functions được kiểm soát ở cyclomatic complexity trung bình (11–20), và (3) cung cấp benchmark Python medium CC với mutation testing đầy đủ bằng MutPy. Đây là ba khoảng trống mà nghiên cứu đề xuất hướng tới giải quyết.