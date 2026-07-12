#!/usr/bin/env python3
"""
compute_branch_coverage.py — Buoc 4 (phan Branch Coverage), khop dung cau truc thuc te:
    functions/PY_XXX.py          <- source that (package, co __init__.py)
    generated_tests/PY-XXX_test.py <- test do GPT sinh ra (luu y: gach ngang, khong phai gach duoi)

QUAN TRONG — PHAT HIEN QUAN TRONG CHO BAO CAO:
    Nhieu test do GPT-4o mini sinh ra (vd PY-005_test.py) KHONG import function that tu
    functions/, ma tu tao mock/class gia rieng va test tren do. Khi do, coverage.py se
    bao branch_coverage = 0% cho function goc — day la KET QUA THAT, khong phai loi do
    luong: no cho thay GPT "ao giac" ra 1 phien ban gia lap thay vi test dung code duoc dua.
    Ghi lai dieu nay o cot 'source_imported' trong output.

CACH DUNG (chay tu THU MUC GOC repo, khong phai tu trong scripts/ hay generated_tests/)
---------
    pip install coverage pytest pandas --break-system-packages

    python scripts\\compute_branch_coverage.py

    # Tuy chon:
    python scripts\\compute_branch_coverage.py --tests-dir generated_tests --functions-dir functions \\
        --out data\\results\\branch_coverage_report.csv --timeout 60

OUTPUT
------
    data/results/branch_coverage_report.csv voi cot:
        function_id, branch_coverage, source_imported, tests_passed, error
"""

import argparse
import json
import os
import subprocess
import sys
from pathlib import Path

import pandas as pd


def id_from_test_filename(fname: str) -> str:
    """PY-005_test.py -> PY-005"""
    return fname[:-len("_test.py")] if fname.endswith("_test.py") else fname


def source_filename_for_id(function_id: str) -> str:
    """PY-005 -> PY_005.py (doi gach ngang -> gach duoi, khop quy uoc functions/)"""
    return function_id.replace("-", "_") + ".py"


def measure_one(test_file: Path, functions_dir: Path, function_id: str, timeout: int) -> dict:
    source_filename = source_filename_for_id(function_id)  # vd: PY_005.py
    source_path = functions_dir / source_filename

    result = {"function_id": function_id, "branch_coverage": None,
              "source_imported": False, "tests_passed": None, "error": ""}

    if not source_path.exists():
        result["error"] = f"Khong tim thay source: {source_path}"
        return result

    cov_json = f"cov_tmp_{function_id.replace('-', '_')}.json"
    cov_data_file = f"coverage_tmp_{function_id.replace('-', '_')}"

    try:
        env = os.environ.copy()
        env["COVERAGE_FILE"] = cov_data_file

        # KHONG dung --include=<path> o day: tren Windows, pattern voi dau "/" co the
        # khong khop duoc voi duong dan noi bo dung dau "\", khien coverage bao
        # "No data collected" cho MOI function du co import dung. Thay vao do, chay
        # coverage --branch KHONG loc gi ca, roi tu tim dung file trong JSON bang ten
        # file (qua pathlib, khong phu thuoc he dieu hanh).
        run_result = subprocess.run(
            ["coverage", "run", "--branch", "-m", "pytest", "-q", "--tb=no", str(test_file)],
            capture_output=True, text=True, timeout=timeout, env=env,
        )
        result["tests_passed"] = run_result.returncode == 0

        subprocess.run(["coverage", "json", "-o", cov_json], capture_output=True, text=True, env=env)

        if not os.path.exists(cov_json):
            result["branch_coverage"] = 0.0
            result["source_imported"] = False
            result["error"] = "Test khong import/goi source that (GPT co the da tu tao mock rieng)"
        else:
            with open(cov_json) as f:
                cov_data = json.load(f)
            # Tim file co ten trung khop VA nam trong thu muc "functions" (qua Path().parts,
            # khong phu thuoc "/" hay "\\")
            file_key = None
            for k in cov_data.get("files", {}):
                kp = Path(k)
                if kp.name == source_filename and "functions" in kp.parts:
                    file_key = k
                    break
            if file_key:
                result["branch_coverage"] = cov_data["files"][file_key]["summary"].get("percent_covered")
                result["source_imported"] = True
            else:
                result["branch_coverage"] = 0.0
                result["source_imported"] = False
                result["error"] = "Test khong import/goi source that (GPT co the da tu tao mock rieng)"
    except FileNotFoundError:
        result["error"] = "Khong tim thay lenh 'coverage' — pip install coverage --break-system-packages"
    except subprocess.TimeoutExpired:
        result["error"] = f"Timeout ({timeout}s)"
    except Exception as e:
        result["error"] = str(e)[:300]
    finally:
        for tmp in [cov_json, cov_data_file]:
            if os.path.exists(tmp):
                os.remove(tmp)

    return result


def main():
    parser = argparse.ArgumentParser(description="Buoc 4 — Do Branch Coverage (khop cau truc functions/ + generated_tests/).")
    parser.add_argument("--tests-dir", default="generated_tests")
    parser.add_argument("--functions-dir", default="functions")
    parser.add_argument("--out", default="data/results/branch_coverage_report.csv")
    parser.add_argument("--timeout", type=int, default=60)
    parser.add_argument("--limit", type=int, default=None)
    args = parser.parse_args()

    tests_dir = Path(args.tests_dir)
    functions_dir = Path(args.functions_dir)

    if not tests_dir.exists():
        print(f"Khong tim thay thu muc: {tests_dir}", file=sys.stderr)
        sys.exit(1)
    if not functions_dir.exists():
        print(f"Khong tim thay thu muc: {functions_dir}", file=sys.stderr)
        sys.exit(1)

    test_files = sorted(tests_dir.glob("*_test.py"))
    if args.limit:
        test_files = test_files[: args.limit]

    rows = []
    n = len(test_files)
    print(f"Chay branch coverage cho {n} test file (nho: chay lenh nay tu thu muc goc repo)...\n")

    for i, test_file in enumerate(test_files):
        function_id = id_from_test_filename(test_file.name)
        print(f"[{i + 1}/{n}] {function_id} ...", end=" ", flush=True)
        res = measure_one(test_file, functions_dir, function_id, args.timeout)
        rows.append(res)
        bc = res["branch_coverage"]
        tag = "OK" if res["source_imported"] else "0% (khong import source that)"
        print(f"BC={bc}%  {'' if res['source_imported'] else tag}" if bc is not None else f"LOI: {res['error']}")

    df = pd.DataFrame(rows)
    os.makedirs(os.path.dirname(args.out) or ".", exist_ok=True)
    df.to_csv(args.out, index=False)

    print("\n" + "=" * 60)
    valid = df["branch_coverage"].dropna()
    if len(valid) > 0:
        print(f"Branch Coverage trung binh: {valid.mean():.2f}% (N={len(valid)})")
        n_imported = df["source_imported"].sum()
        print(f"So function test co import/goi source THAT: {n_imported}/{n} ({n_imported / n * 100:.1f}%)")
        if n_imported < n:
            print(f"[!] {n - n_imported} function co test KHONG cham vao source that — GPT co the da")
            print("    tu tao mock/reimplementation rieng thay vi test code duoc dua. Xem cot 'error'.")
    print(f"\n[Da luu] {args.out}")


if __name__ == "__main__":
    main()
