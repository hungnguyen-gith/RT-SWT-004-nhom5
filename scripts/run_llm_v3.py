#!/usr/bin/env python3
"""
run_llm_v3.py — Sua trigger goc cua van de: prompt zero-shot cu KHONG noi cho GPT biet
phai import ham that tu dau, nen GPT tu bia mock rieng thay vi test code duoc dua.

Script nay:
    1. Doc source THAT truc tiep tu functions/PY_XXX.py (khong qua CSV trung gian).
    2. Prompt BAT BUOC GPT phai `from functions.PY_XXX import <ten_ham>` va GOI ham that,
       KHONG duoc viet lai logic. Neu ham co tham so dau la `self` (method tach tu class),
       huong dan GPT tao 1 stub toi thieu roi goi ham theo kieu unbound: ten_ham(stub, ...).
    3. Self-repair: sau khi sinh test, CHAY THAT bang coverage — kiem tra ca 2 dieu kien:
         a. Test pass (khong loi runtime)
         b. source_imported = True (coverage xac nhan functions/PY_XXX.py THAT SU duoc chay)
       Neu (b) sai du (a) dung (test pass nhung khong dung ham that) -> VAN bi coi la loi,
       gui loi "ban chua goi ham that" nguoc lai cho GPT de sua, lap toi da N lan.

CACH DUNG (chay tu THU MUC GOC repo)
---------
    export OPENAI_API_KEY=sk-...
    pip install openai coverage pytest pandas --break-system-packages

    # Test truoc voi vai function
    python scripts\\run_llm_v3.py --limit 5

    # Full, voi self-repair toi da 3 lan
    python scripts\\run_llm_v3.py --max-repair 3

OUTPUT
------
    generated_tests_v3/PY-XXX_test.py   <- test moi, BAT BUOC import source that
    data/results/llm_output_v3.csv      <- function_id, status, source_imported, branch_coverage, repair_attempts
    data/results/api_log_v3.txt
"""

import argparse
import csv
import json
import os
import random
import re
import subprocess
import sys
import time
from datetime import datetime, timezone
from pathlib import Path

import pandas as pd

try:
    from openai import OpenAI
except ImportError:
    print("Chua cai 'openai'. Chay: pip install openai --break-system-packages", file=sys.stderr)
    sys.exit(1)

MODEL = "gpt-4o-mini-2024-07-18"
TEMPERATURE = 0
MAX_TOKENS = 2048
MAX_RETRIES = 5
PRICE_PER_1M_INPUT = 0.15
PRICE_PER_1M_OUTPUT = 0.60

_model_warned = False


# ---------------------------------------------------------------------------
# Tim ten ham + xay prompt bat buoc import
# ---------------------------------------------------------------------------

def extract_func_name(source_code: str) -> str | None:
    m = re.search(r"^\s*def\s+(\w+)\s*\(", source_code, re.MULTILINE)
    return m.group(1) if m else None


PROMPT_TEMPLATE = """You are a Python testing expert. Write pytest unit tests for the function below.

CRITICAL REQUIREMENT — read carefully:
The function `{func_name}` is defined in the real module `functions.{module_id}`
(importable as: `from functions.{module_id} import {func_name}`).
You MUST import and call this EXACT function in your tests. Do NOT reimplement,
copy, or rewrite the function's logic inside a mock class — that defeats the
purpose of testing the real code and will be REJECTED.

If the function's first parameter is `self` (it was extracted from a class method),
you may still call it directly as an unbound function: create a minimal stub object
that only provides the attributes/methods actually referenced inside the function body
(read the function body below to see what `self.xxx` it uses), then call:
    {func_name}(stub, <other_args>)
This still executes the REAL function body (required for coverage), it just supplies
`self` manually instead of via a real class instance.

Other requirements:
- Use pytest (not unittest)
- Cover normal cases, edge cases, and invalid input where applicable
- Output ONLY valid Python code (the test file content), no explanation, no markdown fences
- Start the file with: from functions.{module_id} import {func_name}

Function to test:
```python
{source_code}
```
"""

REPAIR_PROMPT_NOT_IMPORTED = """Your previous test file for `{func_name}` did NOT actually exercise the real
function code. Either it failed to import `functions.{module_id}`, or it reimplemented
the logic in a mock instead of calling the real function.

Original function (in functions.{module_id}):
```python
{source_code}
```

Your previous test code:
```python
{previous_test_code}
```

Error / reason it was rejected:
```
{error_message}
```

Fix this: your test file MUST start with `from functions.{module_id} import {func_name}`
and MUST call `{func_name}(...)` directly (passing a minimal stub object as the first
argument if the function expects `self`). Output ONLY the corrected, complete, valid
Python test code — no explanation, no markdown fences.
"""


def build_prompt(source_code: str, func_name: str, module_id: str) -> str:
    return PROMPT_TEMPLATE.format(func_name=func_name, module_id=module_id, source_code=source_code)


def build_repair_prompt(source_code: str, func_name: str, module_id: str, previous_test_code: str, error_message: str) -> str:
    return REPAIR_PROMPT_NOT_IMPORTED.format(
        func_name=func_name, module_id=module_id, source_code=source_code,
        previous_test_code=previous_test_code, error_message=error_message[:1000],
    )


def strip_markdown_fences(text: str) -> str:
    text = text.strip()
    if text.startswith("```"):
        lines = text.split("\n")
        if lines[0].startswith("```"):
            lines = lines[1:]
        if lines and lines[-1].strip().startswith("```"):
            lines = lines[:-1]
        text = "\n".join(lines)
    return text.strip()


# ---------------------------------------------------------------------------
# Chay thu test THAT (coverage tren chinh functions/PY_XXX.py) — dung cho self-repair
# ---------------------------------------------------------------------------

def check_test_against_real_source(test_code: str, module_id: str, functions_dir: Path, timeout: int = 30) -> dict:
    """
    Ghi test_code vao 1 file tam trong generated_tests_v3/, chay coverage that tren
    functions/PY_XXX.py, tra ve dict {ok, source_imported, branch_coverage, error}.
    ok=True chi khi source_imported=True VA test pass.
    """
    result = {"ok": False, "source_imported": False, "branch_coverage": None, "tests_passed": False, "error": ""}
    source_filename = f"{module_id}.py"
    tmp_test_path = Path(f"tmp_check_{module_id}_test.py")
    cov_json = f"cov_tmp_{module_id}.json"
    cov_data_file = f"coverage_tmp_{module_id}"

    try:
        tmp_test_path.write_text(test_code, encoding="utf-8")
        env = os.environ.copy()
        env["COVERAGE_FILE"] = cov_data_file

        # KHONG dung --include=<path>: tren Windows pattern "/" co the khong khop duong
        # dan noi bo dung "\\", khien coverage bao "No data" cho MOI truong hop du dung.
        # Thay vao do chay khong loc gi, roi tim file trong JSON bang ten (qua pathlib).
        run_result = subprocess.run(
            ["coverage", "run", "--branch", "-m", "pytest", "-q", "--tb=short", str(tmp_test_path)],
            capture_output=True, text=True, timeout=timeout, env=env,
        )
        result["tests_passed"] = run_result.returncode == 0
        combined_output = (run_result.stdout + "\n" + run_result.stderr).strip()

        subprocess.run(["coverage", "json", "-o", cov_json], capture_output=True, text=True, env=env)
        if os.path.exists(cov_json):
            with open(cov_json) as f:
                cov_data = json.load(f)
            file_key = None
            for k in cov_data.get("files", {}):
                kp = Path(k)
                if kp.name == source_filename and "functions" in kp.parts:
                    file_key = k
                    break
            if file_key:
                result["branch_coverage"] = cov_data["files"][file_key]["summary"].get("percent_covered")
                result["source_imported"] = True

        if not result["source_imported"]:
            result["error"] = "Test khong import/goi source that tu functions." + module_id
        elif not result["tests_passed"]:
            result["error"] = combined_output[-1200:]
        else:
            result["ok"] = True

    except subprocess.TimeoutExpired:
        result["error"] = f"Timeout ({timeout}s)"
    except Exception as e:
        result["error"] = str(e)[:300]
    finally:
        for tmp in [tmp_test_path, cov_json, cov_data_file]:
            p = Path(tmp)
            if p.exists():
                p.unlink()

    return result


# ---------------------------------------------------------------------------
# API voi retry (SS8.2)
# ---------------------------------------------------------------------------

def call_llm_with_retry(client: OpenAI, prompt: str, max_retries: int = MAX_RETRIES):
    for attempt in range(max_retries):
        try:
            return client.chat.completions.create(
                model=MODEL, messages=[{"role": "user", "content": prompt}],
                temperature=TEMPERATURE, max_tokens=MAX_TOKENS,
            )
        except Exception as e:
            if "rate_limit" in str(e).lower() or "429" in str(e):
                wait = (2 ** attempt) + random.uniform(0, 1)
                print(f"    [Retry {attempt + 1}/{max_retries}] Rate limit. Cho {wait:.1f}s")
                time.sleep(wait)
            else:
                raise
    return None


def check_model_drift(response_model: str):
    global _model_warned
    if response_model and response_model != MODEL and not _model_warned:
        print(f"\n  [!] CANH BAO: response.model='{response_model}' khac '{MODEL}'. Bao PL ngay.\n")
        _model_warned = True


def append_result_row(output_csv: str, row: dict, fieldnames: list):
    os.makedirs(os.path.dirname(output_csv) or ".", exist_ok=True)
    is_new = not os.path.exists(output_csv)
    with open(output_csv, "a", encoding="utf-8", newline="") as f:
        writer = csv.DictWriter(f, fieldnames=fieldnames)
        if is_new:
            writer.writeheader()
        writer.writerow(row)


def append_log(log_path: str, function_id: str, model: str, cost: float, status: str, error: str = ""):
    os.makedirs(os.path.dirname(log_path) or ".", exist_ok=True)
    is_new = not os.path.exists(log_path)
    with open(log_path, "a", encoding="utf-8") as f:
        if is_new:
            f.write("timestamp,function_id,model,cost_usd,status,error\n")
        ts = datetime.now(timezone.utc).isoformat()
        f.write(f"{ts},{function_id},{model},{cost:.6f},{status},{error.replace(',', ';').replace(chr(10), ' ')}\n")


def load_done_ids(output_csv: str) -> set:
    if not os.path.exists(output_csv):
        return set()
    try:
        df = pd.read_csv(output_csv)
        return set(df.loc[df["status"].isin(["ok"]), "function_id"].astype(str))
    except Exception:
        return set()


# ---------------------------------------------------------------------------
# Main
# ---------------------------------------------------------------------------

def main():
    parser = argparse.ArgumentParser(description="Prompt bat buoc import source that + self-repair kiem tra source_imported.")
    parser.add_argument("--functions-dir", default="functions")
    parser.add_argument("--output-tests-dir", default="generated_tests_v3")
    parser.add_argument("--output", default="data/results/llm_output_v3.csv")
    parser.add_argument("--log", default="data/results/api_log_v3.txt")
    parser.add_argument("--max-repair", type=int, default=3)
    parser.add_argument("--limit", type=int, default=None)
    args = parser.parse_args()

    api_key = os.environ.get("OPENAI_API_KEY")
    if not api_key:
        print("Chua set OPENAI_API_KEY.", file=sys.stderr)
        sys.exit(1)

    functions_dir = Path(args.functions_dir)
    output_tests_dir = Path(args.output_tests_dir)
    output_tests_dir.mkdir(exist_ok=True, parents=True)

    source_files = sorted(functions_dir.glob("PY_*.py"))
    if args.limit:
        source_files = source_files[: args.limit]

    done_ids = load_done_ids(args.output)
    if done_ids:
        print(f"[Resume] Da co {len(done_ids)} function status=ok, se bo qua.")

    client = OpenAI(api_key=api_key)
    fieldnames = ["function_id", "model", "status", "repair_attempts", "source_imported",
                  "branch_coverage", "test_file", "cost_usd", "elapsed_s", "error"]

    n_total = len(source_files)
    cumulative_cost = 0.0

    for idx, src_file in enumerate(source_files):
        module_id = src_file.stem  # PY_005
        function_id = module_id.replace("_", "-")  # PY-005
        if function_id in done_ids:
            continue

        source_code = src_file.read_text(encoding="utf-8")
        func_name = extract_func_name(source_code)
        if not func_name:
            append_result_row(args.output, {
                "function_id": function_id, "model": MODEL, "status": "error", "repair_attempts": 0,
                "source_imported": False, "branch_coverage": "", "test_file": "", "cost_usd": "0",
                "elapsed_s": "0", "error": "Khong tim thay 'def <ten_ham>(' trong source",
            }, fieldnames)
            print(f"[{idx + 1}/{n_total}] {function_id} ... BO QUA (khong parse duoc ten ham)")
            continue

        print(f"[{idx + 1}/{n_total}] {function_id} (ham: {func_name}) ...", end=" ", flush=True)
        start = time.time()
        prompt = build_prompt(source_code, func_name, module_id)

        repair_attempts = 0
        final_test_code = None
        final_check = {"source_imported": False, "branch_coverage": None, "error": ""}

        try:
            for attempt in range(1 + args.max_repair):
                response = call_llm_with_retry(client, prompt)
                if response is None:
                    final_check["error"] = "Het retry, rate-limit"
                    break

                check_model_drift(getattr(response, "model", MODEL))
                output_text = response.choices[0].message.content
                usage = response.usage
                cost = (usage.prompt_tokens / 1_000_000 * PRICE_PER_1M_INPUT
                        + usage.completion_tokens / 1_000_000 * PRICE_PER_1M_OUTPUT)
                cumulative_cost += cost

                if not output_text or not output_text.strip():
                    final_check["error"] = "Empty response"
                    break

                test_code = strip_markdown_fences(output_text)
                check = check_test_against_real_source(test_code, module_id, functions_dir)
                final_test_code = test_code
                final_check = check

                if check["ok"]:
                    break

                repair_attempts = attempt + 1
                if attempt < args.max_repair:
                    print(f"[repair {attempt + 1}/{args.max_repair}]", end=" ", flush=True)
                    prompt = build_repair_prompt(source_code, func_name, module_id, test_code, check["error"])

            elapsed = time.time() - start

            if final_test_code is None:
                append_result_row(args.output, {
                    "function_id": function_id, "model": MODEL, "status": "INVALID", "repair_attempts": repair_attempts,
                    "source_imported": False, "branch_coverage": "", "test_file": "", "cost_usd": f"{cumulative_cost:.6f}",
                    "elapsed_s": f"{elapsed:.2f}", "error": final_check["error"],
                }, fieldnames)
                append_log(args.log, function_id, MODEL, 0.0, "INVALID", final_check["error"])
                print(f"INVALID ({final_check['error'][:60]})")
                time.sleep(1.0)
                continue

            test_file = output_tests_dir / f"{function_id}_test.py"
            test_file.write_text(final_test_code, encoding="utf-8")

            status = "ok" if final_check["ok"] else "ok_but_not_verified"
            append_result_row(args.output, {
                "function_id": function_id, "model": MODEL, "status": status, "repair_attempts": repair_attempts,
                "source_imported": final_check["source_imported"], "branch_coverage": final_check["branch_coverage"],
                "test_file": str(test_file), "cost_usd": f"{cumulative_cost:.6f}", "elapsed_s": f"{elapsed:.2f}",
                "error": "" if final_check["ok"] else final_check["error"],
            }, fieldnames)
            append_log(args.log, function_id, MODEL, cumulative_cost, status)
            bc = final_check["branch_coverage"]
            print(f"{status} (imported={final_check['source_imported']}, BC={bc}, repair={repair_attempts}, ${cumulative_cost:.4f})")

        except Exception as e:
            elapsed = time.time() - start
            append_result_row(args.output, {
                "function_id": function_id, "model": MODEL, "status": "error", "repair_attempts": repair_attempts,
                "source_imported": False, "branch_coverage": "", "test_file": "", "cost_usd": "0",
                "elapsed_s": f"{elapsed:.2f}", "error": str(e)[:200],
            }, fieldnames)
            append_log(args.log, function_id, MODEL, 0.0, "error", str(e))
            print(f"LOI: {e}")

        time.sleep(1.0)

    print("\n" + "=" * 60)
    print(f"XONG. Tong chi phi: ${cumulative_cost:.4f}")
    print(f"Output: {args.output}")


if __name__ == "__main__":
    main()
