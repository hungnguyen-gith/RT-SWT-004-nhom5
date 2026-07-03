"""
run_llm_experiment.py
======================
Gọi GPT-4o mini (zero-shot, temperature=0.0) để generate unit tests cho N=50
Python functions, đo Branch Coverage bằng coverage.py, tính CSR (Compilation
Success Rate), và log chi phí API cho từng lần gọi.

INPUT (cấu trúc thật của data/full_ground_truth.csv):
    Cột: function_id, language, cc_band, cc_value, source_code,
         annotator_dg, annotator_rw, final_label, notes
    -> source_code chứa TOÀN BỘ code của function trực tiếp trong ô CSV
       (không đọc từ file rời). func_name được tự trích ra bằng regex
       từ dòng `def <tên_hàm>(...)` đầu tiên trong source_code.

OUTPUT:
    results/llm_output.csv   - raw response từ LLM + token usage + cost + latency
    results/bc_csr.csv       - compiled_ok (CSR) + branch_coverage_pct mỗi function

CÁCH CHẠY (Windows CMD):
    set OPENAI_API_KEY=sk-xxxxxxxx
    python run_llm_experiment.py

YÊU CẦU CÀI ĐẶT TRƯỚC:
    pip install openai coverage pytest

⚠️ GIẢ ĐỊNH CẦN BẠN XÁC NHẬN LẠI:
  1. source_code trong CSV không có import phụ thuộc ngoài (re, math, ...). Nếu function
     gốc cần import gì mà không có sẵn trong source_code, compile sẽ lỗi — cần kiểm tra
     thủ công vài dòng đầu của source_code các function bị lỗi CSR.
  2. Tên hàm được trích bằng regex tìm `def <tên>(` ĐẦU TIÊN trong source_code. Nếu 1 ô
     source_code có nhiều def lồng nhau (nested function, helper function), script chỉ
     lấy def ngoài cùng đầu tiên — cần bạn xác nhận đây đúng là hàm cần test.
  3. Giá GPT-4o mini bên dưới (PRICE_INPUT_PER_1M / PRICE_OUTPUT_PER_1M) cần bạn
     double-check lại trên trang pricing chính thức của OpenAI tại thời điểm chạy,
     vì giá có thể đã thay đổi.
"""

import csv
import json
import re
import subprocess
import time
from datetime import datetime
from pathlib import Path

from openai import OpenAI

# ---------------------------------------------------------------------------
# CONFIG
# ---------------------------------------------------------------------------
MODEL = "gpt-4o-mini"
TEMPERATURE = 0.0

INPUT_CSV = Path("data/full_ground_truth.csv")
OUTPUT_DIR = Path("results")
LLM_OUTPUT_CSV = OUTPUT_DIR / "llm_output.csv"
BC_CSR_CSV = OUTPUT_DIR / "bc_csr.csv"
GENERATED_TESTS_DIR = Path("generated_tests")

# Giá GPT-4o mini (USD / 1M tokens) - ⚠️ KIỂM TRA LẠI trước khi chạy thật
PRICE_INPUT_PER_1M = 0.15
PRICE_OUTPUT_PER_1M = 0.60

PROMPT_TEMPLATE = """You are an expert Python test engineer. Write pytest unit tests \
for the following function.

Requirements:
- Output ONLY valid Python code (no markdown fences, no explanation, no comments \
outside the code).
- Use pytest style (functions named test_...).
- Assume the function is importable via: from func_under_test import {func_name}
- Cover normal cases, edge cases, and exception cases if relevant.

Function:
```python
{source_code}
```
"""

client = OpenAI()  # đọc OPENAI_API_KEY từ biến môi trường


# ---------------------------------------------------------------------------
# STEP 1 — Load dataset
# ---------------------------------------------------------------------------
def load_functions(csv_path: Path):
    if not csv_path.exists():
        raise FileNotFoundError(
            f"Không tìm thấy {csv_path}. Kiểm tra lại đường dẫn / bạn có đang "
            "chạy script từ đúng thư mục gốc project không."
        )
    with open(csv_path, newline="", encoding="utf-8") as f:
        return list(csv.DictReader(f))


def extract_func_name(source_code: str) -> str:
    """Trích tên hàm từ dòng `def <ten>(` đầu tiên trong source_code."""
    match = re.search(r"^\s*def\s+(\w+)\s*\(", source_code, re.MULTILINE)
    if match:
        return match.group(1)
    return "unknown_function"


# ---------------------------------------------------------------------------
# STEP 2 — Call GPT-4o mini
# ---------------------------------------------------------------------------
def call_gpt4o_mini(source_code: str, func_name: str) -> dict:
    prompt = PROMPT_TEMPLATE.format(func_name=func_name, source_code=source_code)

    start = time.time()
    response = client.chat.completions.create(
        model=MODEL,
        temperature=TEMPERATURE,
        messages=[{"role": "user", "content": prompt}],
    )
    elapsed = time.time() - start

    content = response.choices[0].message.content
    usage = response.usage
    input_tokens = usage.prompt_tokens
    output_tokens = usage.completion_tokens
    cost = (input_tokens / 1_000_000 * PRICE_INPUT_PER_1M) + (
        output_tokens / 1_000_000 * PRICE_OUTPUT_PER_1M
    )

    return {
        "raw_response": content,
        "input_tokens": input_tokens,
        "output_tokens": output_tokens,
        "cost_usd": round(cost, 6),
        "latency_sec": round(elapsed, 2),
    }


def strip_markdown_fences(code: str) -> str:
    """LLM đôi khi vẫn trả về code kèm ```python ... ``` dù đã dặn không làm vậy."""
    code = code.strip()
    if code.startswith("```"):
        lines = code.split("\n")
        if lines[0].startswith("```"):
            lines = lines[1:]
        if lines and lines[-1].strip().startswith("```"):
            lines = lines[:-1]
        code = "\n".join(lines)
    return code.strip()


# ---------------------------------------------------------------------------
# STEP 3 — Compile check + Branch Coverage
# ---------------------------------------------------------------------------
def run_coverage(func_id: str, source_code: str, test_code: str):
    """
    Ghi function gốc + test LLM sinh ra vào thư mục riêng, compile-check,
    rồi chạy pytest dưới coverage.py (branch mode).
    Trả về: (compiled_ok, branch_coverage_pct, error_log)
    """
    work_dir = GENERATED_TESTS_DIR / func_id
    work_dir.mkdir(parents=True, exist_ok=True)

    module_path = work_dir / "func_under_test.py"
    test_path = work_dir / "test_generated.py"

    module_path.write_text(source_code, encoding="utf-8")
    test_path.write_text(test_code, encoding="utf-8")

    # 1) Compile check (CSR)
    compile_proc = subprocess.run(
        ["python", "-m", "py_compile", str(test_path)],
        cwd=work_dir,
        capture_output=True,
        text=True,
    )
    compiled_ok = compile_proc.returncode == 0
    if not compiled_ok:
        return False, 0.0, compile_proc.stderr[:1000]

    # 2) Run coverage (branch)
    old_cov = work_dir / ".coverage"
    if old_cov.exists():
        old_cov.unlink()

    run_proc = subprocess.run(
        [
            "python", "-m", "coverage", "run",
            "--branch",
            "--source=func_under_test",
            "-m", "pytest", "test_generated.py", "-q",
        ],
        cwd=work_dir,
        capture_output=True,
        text=True,
    )

    subprocess.run(
        ["python", "-m", "coverage", "json", "-o", "coverage.json"],
        cwd=work_dir,
        capture_output=True,
        text=True,
    )

    branch_coverage = 0.0
    coverage_json_path = work_dir / "coverage.json"
    if coverage_json_path.exists():
        try:
            cov_data = json.loads(coverage_json_path.read_text(encoding="utf-8"))
            branch_coverage = cov_data.get("totals", {}).get("percent_covered", 0.0)
        except (json.JSONDecodeError, KeyError):
            pass

    error_log = (run_proc.stdout + run_proc.stderr)[:1000]
    return compiled_ok, branch_coverage, error_log


# ---------------------------------------------------------------------------
# MAIN
# ---------------------------------------------------------------------------
def main():
    OUTPUT_DIR.mkdir(exist_ok=True)
    GENERATED_TESTS_DIR.mkdir(exist_ok=True)

    functions = load_functions(INPUT_CSV)
    print(f"Loaded {len(functions)} functions from {INPUT_CSV}")

    llm_rows = []
    bc_csr_rows = []
    total_cost = 0.0

    for i, row in enumerate(functions, 1):
        func_id = row["function_id"]
        source_code = row["source_code"]
        func_name = extract_func_name(source_code)

        print(f"[{i}/{len(functions)}] {func_id} ({func_name}) ...", end=" ", flush=True)

        if not source_code.strip():
            print("SKIP (source_code rỗng)")
            continue

        try:
            result = call_gpt4o_mini(source_code, func_name)
        except Exception as e:  # lỗi API: rate limit, network, auth...
            print(f"API ERROR: {e}")
            llm_rows.append({
                "func_id": func_id, "func_name": func_name,
                "timestamp": datetime.now().isoformat(),
                "model": MODEL, "temperature": TEMPERATURE,
                "raw_response": "", "input_tokens": 0, "output_tokens": 0,
                "cost_usd": 0, "latency_sec": 0, "error": str(e),
            })
            bc_csr_rows.append({
                "func_id": func_id, "func_name": func_name,
                "compiled_ok": False, "branch_coverage_pct": 0.0,
                "error_log": str(e)[:500],
            })
            continue

        total_cost += result["cost_usd"]

        llm_rows.append({
            "func_id": func_id, "func_name": func_name,
            "timestamp": datetime.now().isoformat(),
            "model": MODEL, "temperature": TEMPERATURE,
            "raw_response": result["raw_response"],
            "input_tokens": result["input_tokens"],
            "output_tokens": result["output_tokens"],
            "cost_usd": result["cost_usd"],
            "latency_sec": result["latency_sec"],
            "error": "",
        })

        test_code = strip_markdown_fences(result["raw_response"])
        compiled_ok, branch_coverage, error_log = run_coverage(func_id, source_code, test_code)

        bc_csr_rows.append({
            "func_id": func_id, "func_name": func_name,
            "compiled_ok": compiled_ok,
            "branch_coverage_pct": branch_coverage,
            "error_log": "" if compiled_ok else error_log,
        })

        print(f"OK (cost=${result['cost_usd']:.6f}, BC={branch_coverage:.1f}%, compiled={compiled_ok})")

    if not llm_rows:
        print("Không có function nào được xử lý — kiểm tra lại input CSV / đường dẫn.")
        return

    with open(LLM_OUTPUT_CSV, "w", newline="", encoding="utf-8") as f:
        writer = csv.DictWriter(f, fieldnames=list(llm_rows[0].keys()))
        writer.writeheader()
        writer.writerows(llm_rows)

    with open(BC_CSR_CSV, "w", newline="", encoding="utf-8") as f:
        writer = csv.DictWriter(f, fieldnames=list(bc_csr_rows[0].keys()))
        writer.writeheader()
        writer.writerows(bc_csr_rows)

    n_compiled = sum(1 for r in bc_csr_rows if r["compiled_ok"])
    csr = (n_compiled / len(bc_csr_rows) * 100) if bc_csr_rows else 0

    print("\n" + "=" * 60)
    print(f"DONE. {len(llm_rows)} functions processed.")
    print(f"Total API cost: ${total_cost:.4f}")
    print(f"CSR (Compilation Success Rate): {csr:.1f}% ({n_compiled}/{len(bc_csr_rows)})")
    print(f"Output: {LLM_OUTPUT_CSV}")
    print(f"Output: {BC_CSR_CSV}")


if __name__ == "__main__":
    main()
