#!/usr/bin/env python3
"""
compute_bc_csr.py — Buoc 4 (LR): voi moi test file GPT sinh ra, thu compile -> ghi CSR (1/0),
chay coverage --branch -m pytest -> ghi BC (branch coverage %).
Du an: Evaluating GPT-4o mini Zero-Shot for Unit Test Generation (Nhom 5)

CSR (Compile Success Rate): 1 neu test code compile duoc (khong loi syntax), 0 neu khong.
BC (Branch Coverage): % nhanh (branch) cua function goc duoc test bao phu, do bang coverage.py.
    - Neu CSR = 0 (khong compile duoc) thi BC luon = 0 (khong chay duoc test).

CACH DUNG
---------
    python scripts/compute_bc_csr.py \\
        --llm-output results/llm_output.csv \\
        --ground-truth data/functions.csv \\
        --out results/bc_csr.csv

YEU CAU
-------
    pip install coverage pytest --break-system-packages
"""

import argparse
import json
import os
import py_compile
import shutil
import subprocess
import sys
import tempfile

import pandas as pd

MODULE_NAME = "func_under_test"


def check_compile(test_code: str) -> tuple[bool, str]:
    """CSR: thu compile code test bang py_compile. Tra ve (compile_ok, error_message)."""
    with tempfile.NamedTemporaryFile(mode="w", suffix=".py", delete=False, encoding="utf-8") as f:
        f.write(test_code)
        tmp_path = f.name
    try:
        py_compile.compile(tmp_path, doraise=True)
        return True, ""
    except py_compile.PyCompileError as e:
        return False, str(e)[:300]
    finally:
        os.unlink(tmp_path)
        cache_dir = os.path.join(os.path.dirname(tmp_path), "__pycache__")
        shutil.rmtree(cache_dir, ignore_errors=True)


def prepare_workdir(source_code: str, test_code: str) -> str:
    """Tao thu muc tam: func_under_test.py (source) + conftest.py (shim import) + test_module.py."""
    workdir = tempfile.mkdtemp(prefix="bccsr_")
    with open(os.path.join(workdir, f"{MODULE_NAME}.py"), "w", encoding="utf-8") as f:
        f.write(source_code)

    conftest = f'''
import builtins
import importlib

_mod = importlib.import_module("{MODULE_NAME}")
for _name in dir(_mod):
    if not _name.startswith("_"):
        setattr(builtins, _name, getattr(_mod, _name))
'''
    with open(os.path.join(workdir, "conftest.py"), "w", encoding="utf-8") as f:
        f.write(conftest)

    with open(os.path.join(workdir, "test_module.py"), "w", encoding="utf-8") as f:
        f.write(test_code)

    return workdir


def run_branch_coverage(workdir: str, timeout: int = 60) -> tuple[float | None, str]:
    """Chay pytest duoi coverage --branch, tra ve (% branch coverage, error)."""
    try:
        subprocess.run(
            ["coverage", "run", "--branch", f"--include=*{MODULE_NAME}.py",
             "-m", "pytest", "-q", "--tb=line", "test_module.py"],
            cwd=workdir, capture_output=True, text=True, timeout=timeout,
        )
        json_path = os.path.join(workdir, "cov.json")
        subprocess.run(["coverage", "json", "-o", "cov.json"], cwd=workdir, capture_output=True, text=True, timeout=timeout)
        if not os.path.exists(json_path):
            return None, "Khong sinh duoc cov.json"
        with open(json_path) as f:
            cov_data = json.load(f)
        file_key = next((k for k in cov_data.get("files", {}) if k.endswith(f"{MODULE_NAME}.py")), None)
        if not file_key:
            return 0.0, "func_under_test.py khong duoc goi trong test (0% coverage)"
        return cov_data["files"][file_key]["summary"].get("percent_covered"), ""
    except FileNotFoundError:
        return None, "Khong tim thay lenh 'coverage' — pip install coverage --break-system-packages"
    except subprocess.TimeoutExpired:
        return None, f"Timeout ({timeout}s)"
    except Exception as e:
        return None, str(e)[:300]


def main():
    parser = argparse.ArgumentParser(description="Buoc 4 (LR) — tinh CSR + Branch Coverage.")
    parser.add_argument("--llm-output", default="results/llm_output.csv", help="CSV tu run_llm.py")
    parser.add_argument("--ground-truth", default="data/functions.csv", help="CSV chua source_code goc")
    parser.add_argument("--out", default="results/bc_csr.csv", help="CSV output (function_id,csr,branch_coverage,error)")
    parser.add_argument("--timeout", type=int, default=60, help="Timeout (giay) cho moi function")
    args = parser.parse_args()

    for path, label in [(args.llm_output, "--llm-output"), (args.ground_truth, "--ground-truth")]:
        if not os.path.exists(path):
            print(f"Khong tim thay file cho {label}: {path}", file=sys.stderr)
            sys.exit(1)

    llm_df = pd.read_csv(args.llm_output)
    gt_df = pd.read_csv(args.ground_truth)[["function_id", "source_code"]]
    merged = llm_df.merge(gt_df, on="function_id", how="inner")

    rows = []
    n = len(merged)
    n_compile_ok = 0
    for i, row in merged.iterrows():
        function_id = row["function_id"]
        print(f"[{i + 1}/{n}] {function_id} ...", end=" ", flush=True)

        if row.get("status") != "ok" or not isinstance(row.get("test_file"), str) or not os.path.exists(row["test_file"]):
            print("BO QUA (khong co test tu run_llm.py, xem status='error')")
            rows.append({"function_id": function_id, "csr": 0, "branch_coverage": 0, "error": "missing test_file (run_llm.py loi truoc do)"})
            continue

        with open(row["test_file"], encoding="utf-8") as f:
            test_code = f.read()

        compile_ok, compile_err = check_compile(test_code)
        csr = 1 if compile_ok else 0

        if not compile_ok:
            rows.append({"function_id": function_id, "csr": 0, "branch_coverage": 0, "error": f"compile error: {compile_err}"})
            print(f"CSR=0 (loi compile)")
            n_compile_ok += 0
            continue

        n_compile_ok += 1
        workdir = prepare_workdir(row["source_code"], test_code)
        try:
            bc, err = run_branch_coverage(workdir, timeout=args.timeout)
            rows.append({"function_id": function_id, "csr": 1, "branch_coverage": bc, "error": err})
            print(f"CSR=1, BC={bc if bc is not None else 'N/A'}")
        finally:
            shutil.rmtree(workdir, ignore_errors=True)

    result_df = pd.DataFrame(rows)
    os.makedirs(os.path.dirname(args.out) or ".", exist_ok=True)
    result_df.to_csv(args.out, index=False)

    print("\n" + "=" * 60)
    print(f"XONG. N = {n}")
    print(f"CSR (Compile Success Rate) = {n_compile_ok}/{n} = {n_compile_ok / n * 100:.1f}%")
    valid_bc = result_df.loc[result_df["csr"] == 1, "branch_coverage"].dropna()
    if len(valid_bc) > 0:
        print(f"Branch Coverage (chi tinh tren function CSR=1): mean={valid_bc.mean():.2f}% "
              f"| std={valid_bc.std():.2f} | min={valid_bc.min():.2f} | max={valid_bc.max():.2f} | N={len(valid_bc)}")
    print(f"\n[Da luu] {args.out}")


if __name__ == "__main__":
    main()
