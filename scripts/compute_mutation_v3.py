#!/usr/bin/env python3
"""
compute_mutation_v3.py — Do Mutation Score cho generated_tests_v3/ (test co import source that).

KHAC VOI compute_mutation.py (BAN CU):
    Ban cu tao thu muc tam co lap (khong co package 'functions') + "shim" bom ten ham vao
    builtins — chi hop voi test KHONG import gi ca. Nhung generated_tests_v3/ co dong
    `from functions.PY_XXX import <ten_ham>` that su, nen PHAI chay ngay tai THU MUC GOC
    repo (noi co san package functions/), khong dung thu muc tam nua — neu khong se bi
    ImportError: No module named 'functions'.

    Vi mutmut mutate TRUC TIEP tren file that trong functions/ (tam thoi, roi revert lai),
    script nay xoa .mutmut-cache truoc MOI function de tranh nham lan ket qua giua cac lan chay.

CACH DUNG (BAT BUOC chay tu THU MUC GOC repo)
---------
    pip install "mutmut==2.4.4" --break-system-packages

    python scripts\\compute_mutation_v3.py \\
        --llm-output data\\results\\llm_output_v3.csv \\
        --out data\\results\\mutation_score_v3.csv

    # Test truoc voi vai function (mutation testing cham hon branch coverage nhieu)
    python scripts\\compute_mutation_v3.py --llm-output data\\results\\llm_output_v3.csv \\
        --out data\\results\\mutation_score_v3.csv --limit 3
"""

import argparse
import os
import shutil
import subprocess
import sys
import time
from pathlib import Path

import pandas as pd


def count_ids(status: str, timeout: int = 30) -> int:
    r = subprocess.run(["mutmut", "result-ids", status], capture_output=True, text=True, timeout=timeout)
    out = r.stdout.strip()
    return len(out.split()) if out else 0


def run_mutation_for_function(function_id: str, functions_dir: str, tests_dir: str, timeout: int) -> dict:
    module_id = function_id.replace("-", "_")
    source_rel = f"{functions_dir}/{module_id}.py"
    test_rel = f"{tests_dir}/{function_id}_test.py"

    result = {"killed": None, "survived": None, "timeout_mutants": None,
              "total_mutants": None, "mutation_score": None, "error": ""}

    if not Path(source_rel).exists():
        result["error"] = f"Khong tim thay source: {source_rel}"
        return result
    if not Path(test_rel).exists():
        result["error"] = f"Khong tim thay test: {test_rel}"
        return result

    # Xoa cache cu truoc moi function, tranh mutmut tron lan ket qua cua function truoc
    shutil.rmtree(".mutmut-cache", ignore_errors=True)

    try:
        run_result = subprocess.run(
            ["mutmut", "run",
             "--paths-to-mutate", source_rel,
             "--tests-dir", tests_dir,
             "--runner", f"python -m pytest -q -x --tb=no {test_rel}"],
            capture_output=True, text=True, timeout=timeout,
        )
        killed = count_ids("killed")
        survived = count_ids("survived")
        timed_out = count_ids("timeout") + count_ids("suspicious")

        result["killed"] = killed
        result["survived"] = survived
        result["timeout_mutants"] = timed_out
        result["total_mutants"] = killed + survived + timed_out
        valid = killed + survived
        result["mutation_score"] = (killed / valid * 100) if valid > 0 else None
        if result["total_mutants"] == 0:
            # In ra loi that (thuong bi che boi capture_output) de biet chinh xac nguyen nhan
            debug_output = (run_result.stdout + "\n" + run_result.stderr).strip()
            result["error"] = "Khong sinh duoc mutant. Chi tiet: " + debug_output[-500:]
    except FileNotFoundError:
        result["error"] = "Khong tim thay lenh 'mutmut' — pip install \"mutmut==2.4.4\" --break-system-packages"
    except subprocess.TimeoutExpired:
        result["error"] = f"Timeout ({timeout}s)"
    except Exception as e:
        result["error"] = str(e)[:300]
    finally:
        shutil.rmtree(".mutmut-cache", ignore_errors=True)

    return result


def main():
    parser = argparse.ArgumentParser(description="Do Mutation Score cho generated_tests_v3 (chay tu thu muc goc repo).")
    parser.add_argument("--llm-output", required=True, help="CSV tu run_llm_v3.py (data/results/llm_output_v3.csv)")
    parser.add_argument("--functions-dir", default="functions")
    parser.add_argument("--tests-dir", default="generated_tests_v3")
    parser.add_argument("--out", required=True)
    parser.add_argument("--only-imported", action="store_true", default=True,
                         help="Chi chay mutation cho function co source_imported=True (mac dinh bat, khuyen nghi)")
    parser.add_argument("--timeout", type=int, default=120)
    parser.add_argument("--limit", type=int, default=None)
    args = parser.parse_args()

    if not os.path.exists(args.llm_output):
        print(f"Khong tim thay: {args.llm_output}", file=sys.stderr)
        sys.exit(1)
    if not Path(args.functions_dir).exists():
        print(f"Khong tim thay thu muc {args.functions_dir} — nho chay lenh nay TU THU MUC GOC repo.", file=sys.stderr)
        sys.exit(1)

    df = pd.read_csv(args.llm_output)
    df = df.drop_duplicates(subset="function_id", keep="last")
    df = df[df["status"].isin(["ok", "ok_but_not_verified"])]
    if args.only_imported and "source_imported" in df.columns:
        before = len(df)
        df = df[df["source_imported"].astype(str).isin(["True", "true", "1", "1.0"])]
        print(f"[Loc theo source_imported=True] {before} -> {len(df)} function")

    if args.limit:
        df = df.head(args.limit)

    rows = []
    n = len(df)
    print(f"\nSap chay mutation testing cho {n} function (~15-40s/function, chay TUAN TU tung function).\n")

    for i, row in enumerate(df.itertuples()):
        function_id = row.function_id
        print(f"[{i + 1}/{n}] {function_id} ...", end=" ", flush=True)
        t0 = time.time()
        res = run_mutation_for_function(function_id, args.functions_dir, args.tests_dir, args.timeout)
        elapsed = time.time() - t0
        rows.append({"function_id": function_id, **res})
        ms = res["mutation_score"]
        print(f"mutation_score={ms:.1f}%  ({elapsed:.1f}s)" if ms is not None else f"N/A ({res['error']})  ({elapsed:.1f}s)")

    result_df = pd.DataFrame(rows)
    os.makedirs(os.path.dirname(args.out) or ".", exist_ok=True)
    result_df.to_csv(args.out, index=False)

    print("\n" + "=" * 60)
    valid = result_df["mutation_score"].dropna()
    if len(valid) > 0:
        print(f"Mutation Score trung binh: {valid.mean():.2f}% (N={len(valid)})")
        print(f"  min={valid.min():.2f}% max={valid.max():.2f}% std={valid.std():.2f}")
    else:
        print("Khong co function nao tinh duoc mutation score — xem cot 'error'.")
    print(f"\n[Da luu] {args.out}")


if __name__ == "__main__":
    main()
