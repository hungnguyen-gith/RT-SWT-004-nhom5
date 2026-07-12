#!/usr/bin/env python3
"""
run_llm.py — Buoc 2+3 (LR) + SS8.2 "Chay LLM toan bo": goi GPT-4o mini cho tung function
trong data/functions.csv, luu output JSON + CSV tong hop, log timestamp/model/cost/errors.
Du an: Evaluating GPT-4o mini Zero-Shot for Unit Test Generation (Nhom 5)

Config (theo LR plan, dung CHUNG cho pilot va full):
    model       = gpt-4o-mini-2024-07-18
    temperature = 0
    max_tokens  = 2048
    prompt      = zero-shot Python/pytest (proposal SS5.3)

CACH DUNG
---------
    export OPENAI_API_KEY=sk-...

    # Pilot (chay truoc)
    python scripts/run_llm.py --input data/pilot_sample.csv \\
        --output results/pilot_llm_output.csv --log results/pilot_api_log.txt

    # Full (SS8.2 — cung config nhu pilot)
    python scripts/run_llm.py --input data/functions.csv \\
        --output results/full_llm_output.csv --log results/full_api_log.txt

Resume duoc: neu function_id da co status=ok trong output CSV thi bo qua, khong goi lai API.
Sau moi batch lon: nho commit len GitHub (khong de mat data neu bi ngat giua chung).

XU LY LOI API (SS8.2)
----------------------
    - Empty response      -> danh dau status=INVALID, KHONG tu dien/bia noi dung test.
    - Rate limit (429)    -> retry voi exponential backoff (2**attempt + jitter), toi da 5 lan.
    - Loi khac (khong phai rate limit) -> KHONG retry, ghi status=error va di tiep function ke.
    - response.model khac voi model da request luc dau -> in CANH BAO ngay (bao PL).
"""

import argparse
import csv
import json
import os
import random
import sys
import time
from datetime import datetime, timezone

import pandas as pd

try:
    from openai import OpenAI
except ImportError:
    print("Chua cai package 'openai'. Chay: pip install openai --break-system-packages", file=sys.stderr)
    sys.exit(1)

MODEL = "gpt-4o-mini-2024-07-18"
TEMPERATURE = 0
MAX_TOKENS = 2048
MAX_RETRIES = 5

PRICE_PER_1M_INPUT = 0.15
PRICE_PER_1M_OUTPUT = 0.60

# Neu response.model tra ve khac model nay -> co the API tu dong doi version -> canh bao ngay
_model_warned = False

ZERO_SHOT_PROMPT_TEMPLATE = """You are a Python testing expert. Write pytest unit tests for the function below.
Requirements:
- Use pytest (not unittest)
- Cover normal cases, edge cases, and invalid input where applicable
- Output ONLY valid Python code (the test file content), no explanation, no markdown fences

Function to test:
```python
{source_code}
```
"""


def build_prompt(source_code: str) -> str:
    return ZERO_SHOT_PROMPT_TEMPLATE.format(source_code=source_code)


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


def load_done_ids(output_csv: str) -> set:
    if not os.path.exists(output_csv):
        return set()
    try:
        df = pd.read_csv(output_csv)
        return set(df.loc[df["status"] == "ok", "function_id"].astype(str))
    except Exception:
        return set()


def append_result_row(output_csv: str, row: dict, fieldnames: list):
    os.makedirs(os.path.dirname(output_csv) or ".", exist_ok=True)
    is_new = not os.path.exists(output_csv)
    with open(output_csv, "a", encoding="utf-8", newline="") as f:
        writer = csv.DictWriter(f, fieldnames=fieldnames)
        if is_new:
            writer.writeheader()
        writer.writerow(row)


def append_log(log_path: str, function_id: str, model: str, cost: float, status: str, error: str = ""):
    """Ghi 1 dong vao log (SS8.2): timestamp, response.model (model THAT tra ve), cost, errors."""
    os.makedirs(os.path.dirname(log_path) or ".", exist_ok=True)
    is_new = not os.path.exists(log_path)
    with open(log_path, "a", encoding="utf-8") as f:
        if is_new:
            f.write("timestamp,function_id,model,cost_usd,status,error\n")
        ts = datetime.now(timezone.utc).isoformat()
        error_clean = error.replace(",", ";").replace("\n", " ")
        f.write(f"{ts},{function_id},{model},{cost:.6f},{status},{error_clean}\n")


def call_llm_with_retry(client: OpenAI, prompt: str, max_retries: int = MAX_RETRIES):
    """
    Goi API voi retry exponential backoff (SS8.2), chi retry khi la loi rate-limit (429).
    Loi khac -> raise ngay, khong retry.
    Tra ve response hoac None neu het retry (van la rate-limit sau max_retries lan).
    """
    for attempt in range(max_retries):
        try:
            response = client.chat.completions.create(
                model=MODEL,
                messages=[{"role": "user", "content": prompt}],
                temperature=TEMPERATURE,
                max_tokens=MAX_TOKENS,
            )
            return response
        except Exception as e:
            if "rate_limit" in str(e).lower() or "429" in str(e):
                wait = (2 ** attempt) + random.uniform(0, 1)  # 1s, 2s, 4s, 8s, 16s + jitter
                print(f"    [Retry {attempt + 1}/{max_retries}] Rate limit hit. Cho {wait:.1f}s roi thu lai")
                time.sleep(wait)
            else:
                raise  # loi khac -> khong retry, day len cho ham goi xu ly
    return None  # het retry -> van la rate-limit -> danh dau INVALID o ngoai


def check_model_drift(response_model: str):
    """SS8.2: neu response.model khac model da request -> canh bao ngay (bao PL)."""
    global _model_warned
    if response_model and response_model != MODEL and not _model_warned:
        print(f"\n  [!] CANH BAO: API tra ve model='{response_model}', khac voi model da request='{MODEL}'.")
        print(f"      -> Format response co the da thay doi giua chung. BAO PL NGAY truoc khi chay tiep.\n")
        _model_warned = True


def main():
    parser = argparse.ArgumentParser(description="Buoc 2+3 (LR) — batch goi GPT-4o mini, luu JSON + CSV.")
    parser.add_argument("--input", default="data/functions.csv", help="CSV chua function_id + source_code")
    parser.add_argument("--output", default="results/llm_output.csv", help="CSV tong hop ket qua")
    parser.add_argument("--log", default="results/full_api_log.txt", help="Log timestamp/model/cost/errors (SS8.2)")
    parser.add_argument("--json-dir", default="results/llm_raw", help="Thu muc luu output JSON tho tung function")
    parser.add_argument("--tests-dir", default="results/generated_tests", help="Thu muc luu code test da tach ra (dung cho Buoc 4)")
    parser.add_argument("--limit", type=int, default=None, help="Chi chay N function dau (debug)")
    args = parser.parse_args()

    api_key = os.environ.get("OPENAI_API_KEY")
    if not api_key:
        print("Chua set bien moi truong OPENAI_API_KEY. Chay: export OPENAI_API_KEY=sk-...", file=sys.stderr)
        sys.exit(1)

    if not os.path.exists(args.input):
        print(f"Khong tim thay file input: {args.input}", file=sys.stderr)
        print("  -> Neu chua co data/functions.csv, tao tu file co san, vd (PowerShell):")
        print('     Copy-Item data\\full_ground_truth.csv data\\functions.csv')
        sys.exit(1)

    df = pd.read_csv(args.input)
    if "function_id" not in df.columns or "source_code" not in df.columns:
        print("CSV input can co cot 'function_id' va 'source_code'.", file=sys.stderr)
        sys.exit(1)

    if args.limit:
        df = df.head(args.limit)

    os.makedirs(args.json_dir, exist_ok=True)
    os.makedirs(args.tests_dir, exist_ok=True)

    done_ids = load_done_ids(args.output)
    if done_ids:
        print(f"[Resume] Da co {len(done_ids)} function status=ok trong {args.output}, se bo qua.")

    client = OpenAI(api_key=api_key)
    fieldnames = ["function_id", "model", "status", "json_file", "test_file",
                  "prompt_tokens", "completion_tokens", "total_tokens", "cost_usd", "elapsed_s", "error"]

    n_total = len(df)
    cumulative_cost = 0.0

    for idx, row in df.iterrows():
        function_id = str(row["function_id"])
        source_code = str(row["source_code"])

        if function_id in done_ids:
            continue

        print(f"[{idx + 1}/{n_total}] {function_id} ...", end=" ", flush=True)
        prompt = build_prompt(source_code)
        start = time.time()
        try:
            response = call_llm_with_retry(client, prompt)
            elapsed = time.time() - start

            if response is None:
                # Het retry, van la rate-limit -> danh dau INVALID, KHONG tu bia noi dung
                append_result_row(args.output, {
                    "function_id": function_id, "model": MODEL, "status": "INVALID",
                    "json_file": "", "test_file": "", "prompt_tokens": "", "completion_tokens": "",
                    "total_tokens": "", "cost_usd": "0", "elapsed_s": f"{elapsed:.2f}",
                    "error": f"Het {MAX_RETRIES} lan retry, van bi rate-limit",
                }, fieldnames)
                append_log(args.log, function_id, MODEL, 0.0, "INVALID", "rate-limit sau max retries")
                print("INVALID (het retry, rate-limit)")
                time.sleep(1.0)
                continue

            response_model = getattr(response, "model", MODEL)
            check_model_drift(response_model)

            output_text = response.choices[0].message.content
            usage = response.usage
            cost = (
                usage.prompt_tokens / 1_000_000 * PRICE_PER_1M_INPUT
                + usage.completion_tokens / 1_000_000 * PRICE_PER_1M_OUTPUT
            )
            cumulative_cost += cost

            # SS8.2: Empty response -> danh dau INVALID, KHONG tu dien/bia noi dung
            if not output_text or not output_text.strip():
                append_result_row(args.output, {
                    "function_id": function_id, "model": response_model, "status": "INVALID",
                    "json_file": "", "test_file": "",
                    "prompt_tokens": usage.prompt_tokens, "completion_tokens": usage.completion_tokens,
                    "total_tokens": usage.total_tokens, "cost_usd": f"{cost:.6f}",
                    "elapsed_s": f"{elapsed:.2f}", "error": "Empty response tu API",
                }, fieldnames)
                append_log(args.log, function_id, response_model, cost, "INVALID", "empty response")
                print("INVALID (empty response)")
                time.sleep(1.0)
                continue

            # Luu JSON tho (Buoc 2: "luu output JSON")
            json_file = os.path.join(args.json_dir, f"{function_id}.json")
            with open(json_file, "w", encoding="utf-8") as f:
                json.dump({
                    "function_id": function_id,
                    "model": response_model,
                    "timestamp": datetime.now(timezone.utc).isoformat(),
                    "prompt": prompt,
                    "response_text": output_text,
                    "usage": {
                        "prompt_tokens": usage.prompt_tokens,
                        "completion_tokens": usage.completion_tokens,
                        "total_tokens": usage.total_tokens,
                    },
                    "cost_usd": cost,
                }, f, ensure_ascii=False, indent=2)

            # Tach rieng code test (dung cho Buoc 4: compile check + coverage)
            test_code = strip_markdown_fences(output_text)
            test_file = os.path.join(args.tests_dir, f"{function_id}_test.py")
            with open(test_file, "w", encoding="utf-8") as f:
                f.write(test_code)

            append_result_row(args.output, {
                "function_id": function_id,
                "model": response_model,
                "status": "ok",
                "json_file": json_file,
                "test_file": test_file,
                "prompt_tokens": usage.prompt_tokens,
                "completion_tokens": usage.completion_tokens,
                "total_tokens": usage.total_tokens,
                "cost_usd": f"{cost:.6f}",
                "elapsed_s": f"{elapsed:.2f}",
                "error": "",
            }, fieldnames)
            append_log(args.log, function_id, response_model, cost, "ok")

            print(f"OK ({usage.total_tokens} tok, ${cost:.5f}, cong don ${cumulative_cost:.4f})")

        except Exception as e:
            elapsed = time.time() - start
            append_result_row(args.output, {
                "function_id": function_id,
                "model": MODEL,
                "status": "error",
                "json_file": "",
                "test_file": "",
                "prompt_tokens": "",
                "completion_tokens": "",
                "total_tokens": "",
                "cost_usd": "0",
                "elapsed_s": f"{elapsed:.2f}",
                "error": str(e)[:200],
            }, fieldnames)
            append_log(args.log, function_id, MODEL, 0.0, "error", str(e))
            print(f"LOI: {e}")

        time.sleep(1.0)

    print("\n" + "=" * 60)
    print(f"XONG. Tong chi phi (cong don): ${cumulative_cost:.4f}")
    print(f"Output: {args.output}")
    print(f"Log:    {args.log}")
    print(f"JSON:   {args.json_dir}/")
    print(f"Tests:  {args.tests_dir}/")
    print("\n[Nho] Commit len GitHub ngay sau batch nay (SS8.2), khong de mat data.")
    print("[Buoc tiep theo] python scripts/compute_bc_csr.py")


if __name__ == "__main__":
    main()
