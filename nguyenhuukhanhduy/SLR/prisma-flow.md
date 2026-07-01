# PRISMA Flow — LLM for Unit Test Case Generation
**Thành viên:** Nguyễn Hữu Khánh Duy
---

## Sơ đồ PRISMA

```
[Records từ database searching (N = 122)]   ← Tổng từ search-log.md (129 - 7 snowball)
         ↓
         + Snowballing (N = 7)
         ↓
[Tổng trước dedup (N = 129)]
         ↓
[Sau khi xóa duplicate (N = 22)]   ← = dòng trong 01_all_records.csv
         ↓
┌─────────────────────────────────────────┐
│  Screened title + abstract (N = 22)     │
│  └─ Excluded (N = 1): EC-N=1            │
└─────────────────────────────────────────┘
         ↓ 21 papers pass   ← = INCLUDE trong 02
┌─────────────────────────────────────────┐
│  Full-text assessed (N = 21)            │
│  └─ Excluded (N = 1): EC-O=1            │
└─────────────────────────────────────────┘
         ↓
[Final included (N = 20)]   ← = Include trong 03_final_included.csv
```

---

## Kiểm tra nhất quán (tự check trước khi nộp)

```
Rows trong 01 CSV = N sau dedup              → 22 ✓
Count(v1_decision = EXCLUDE) trong 02 = 1   → Excluded vòng 1 ✓
Count(v1 = INCLUDE) = Full-text assessed = 21 ✓
Count(v2_decision = Include) trong 03 = 20  → Final included ✓
Count(v2_decision = Exclude) trong 03 = 1   → Excluded vòng 2 ✓
```

---

## Chi tiết lý do loại

### V1 Excluded (N = 1) — title + abstract screening

| ID | Tiêu đề (rút gọn) | EC code |
|----|-------------------|---------|
| 22 | Software Testing with Large Language Models: Survey... (Wang 2024) | EC-N: survey/secondary study, không có thực nghiệm gốc |

### V2 Excluded (N = 1) — full-text screening

| ID | Tiêu đề (rút gọn) | EC/IC code |
|----|-------------------|-----------|
| 20 | An Exploratory Study on Using LLMs for Mutation Testing (2024) | EC-O: paper về sinh MUTANT bằng LLM, không phải sinh unit test cases |
