# data/raw/ — Raw Dataset Source (immutable)

Provenance for the dataset in `../full_ground_truth.csv`, `../pilot_sample.csv`,
`../pilot_ground_truth.csv`. **Do not edit** the raw source — treat as read-only input.

This file records where the data came from, the filtering method, the CSV column
layout, and the download date.

- **Download / pin date:** 2026-06-27
- **Source:** [CodeXGLUE](https://github.com/microsoft/CodeXGLUE) — GitHub tự crawl
- **CC measuring / filtering tool:** `Radon`
- **Complexity band:** Cyclomatic Complexity 5–15
- **Language:** Python only
- **N = 50** independent functions

## Sampling method

1. Crawl Python functions from CodeXGLUE
2. Filter by Radon: keep only functions with 5 ≤ CC ≤ 15
3. Remove duplicates / functions with cross-dependencies (đảm bảo tính độc lập)
4. Random sample down to N = 50 if pool is larger

## Baseline (Pynguin) config — for reference

- Tool: Pynguin v0.39
- Algorithm: DYNAMOSA
- seed = 42 | time-limit = 60s
- criterion = coverage BRANCH
- Automatically generated asserts
- Rationale: cấu hình thống nhất (seed=42, time-limit=60s) để đảm bảo tính tái lập và công bằng so với chi phí API GPT-4o mini

## Column layout — `full_ground_truth.csv` / `pilot_sample.csv`

| Column | Meaning |
|---|---|
| `func_id` | Unique id (e.g. `PY-001`) |
| `source_repo` | Origin repo/module from CodeXGLUE |
| `file` | Path of the source file the function was mined from |
| `func_name` | Function name |
| `cc` | Cyclomatic complexity (5–15, Radon) |
| `nloc` | Lines of code |
| `params` | Parameter count |
| `start_line`, `end_line` | Span of the function in the source file |
| `raw_source_path` | Path to the extracted single-function file (LLM input) |

## Extra columns — `pilot_ground_truth.csv`

Above columns **plus** empty annotation columns to be filled by hand (≥2 annotators → IAA):
`annotator_dg`, `annotator_rw`, `final_label`, `notes`.

## Note

> `[CẦN CẬP NHẬT]` — nếu có random seed riêng cho bước sample N=50 (khác với seed=42
> của Pynguin), ghi rõ tại đây để đảm bảo tái lập được.