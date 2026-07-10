# PRISMA Flow – LLM for Unit Test Case Generation
**Thành viên:** Nguyễn Hùng (SE180765)

---

## Sơ đồ PRISMA

```
Records từ database searching (N = 767)
  ├── IEEE Xplore / String A         = 20
  ├── ACM Digital Library / String B = 208
  ├── Semantic Scholar / String C    = 40
  ├── Google Scholar / String D      = 347
  └── OpenAlex / String E            = 152

Sau khi xóa duplicate (N = 62)
         ↓
Screened title + abstract (N = 62)
  └── Excluded (N = 36):
        ├── IC-V (arXiv preprint)           = 10
        ├── IC-V (thesis/repository)        = 8
        ├── EC-O (off topic)                = 9
        ├── IC-I (không dùng LLM)           = 3
        ├── IC-R (abstract trống)           = 2
        ├── IC-Y (năm trống)                = 1
        └── EC-O (JavaScript, năm trống)    = 3
         ↓
Full-text assessed (N = 26)
  └── Excluded (N = 18):
        ├── IC-T (agent/RL/multi-agent)     = 6
        ├── IC-M (không có branch/mutation) = 4
        ├── IC-Lang (đa ngôn ngữ)           = 3
        └── EC-A (không truy cập full-text) = 5
         ↓
Included (N = 8) → 03_final_included.csv
```

---

## Kiểm tra nhất quán

- [x] Tổng từ database = 767 ✓
- [x] Sau dedup = 62 ✓
- [x] V1 EXCLUDE = 36 → V1 INCLUDE = 26 ✓
- [x] V2 EXCLUDE = 18 → V2 INCLUDE = 8 ✓
- [x] Count(v2_decision = INCLUDE) trong 02 = 8 ✓
- [x] Count trong 03_final_included = 8 ✓
