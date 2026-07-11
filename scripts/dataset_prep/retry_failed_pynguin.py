"""
Chay lai CHI CAC FUNCTION BI FAIL trong lan chay Pynguin truoc, dua tren
data/results/pynguin_batch_log.csv. Ket qua duoc CAP NHAT lai vao cung
file log (khong ghi de function da OK).

Usage:
    python retry_failed_pynguin.py
"""
import csv
import os
import subprocess
import sys
import time
from pathlib import Path

MANIFEST = Path("data/functions_manifest.csv")
LOG_PATH = Path("data/results/pynguin_batch_log.csv")
PROJECT_PATH = Path("functions")
OUTPUT_PATH = Path("baseline/pynguin_tests")
ALGORITHM = "DYNAMOSA"
SEED = 42
MAX_SEARCH_TIME = 60


def run_one(module_name: str) -> dict:
    env = os.environ.copy()
    env["PYNGUIN_DANGER_AWARE"] = "1"
    cmd = [
        "pynguin",
        "--project-path", str(PROJECT_PATH),
        "--module-name", module_name,
        "--output-path", str(OUTPUT_PATH),
        "--algorithm", ALGORITHM,
        "--seed", str(SEED),
        "--maximum-search-time", str(MAX_SEARCH_TIME),
    ]
    start = time.time()
    try:
        result = subprocess.run(
            cmd, env=env, capture_output=True, text=True, timeout=MAX_SEARCH_TIME + 60
        )
        elapsed = time.time() - start
        test_file = OUTPUT_PATH / f"test_{module_name}.py"
        return {
            "return_code": result.returncode,
            "elapsed_seconds": round(elapsed, 1),
            "test_file_generated": test_file.exists(),
            "stderr_tail": result.stderr[-800:],
            "stdout_tail": result.stdout[-800:],
        }
    except subprocess.TimeoutExpired:
        elapsed = time.time() - start
        return {
            "return_code": -1,
            "elapsed_seconds": round(elapsed, 1),
            "test_file_generated": False,
            "stderr_tail": "TIMEOUT",
            "stdout_tail": "",
        }


def main():
    if not LOG_PATH.exists():
        print(f"ERROR: khong tim thay {LOG_PATH}. Chay run_pynguin_batch.py truoc.")
        sys.exit(1)

    with open(LOG_PATH, newline="", encoding="utf-8") as f:
        log_rows = list(csv.DictReader(f))

    manifest_by_id = {}
    with open(MANIFEST, newline="", encoding="utf-8") as f:
        for row in csv.DictReader(f):
            manifest_by_id[row["function_id"]] = row

    failed = [r for r in log_rows if r["test_file_generated"] != "True"]
    print(f"Tim thay {len(failed)} function bi fail lan truoc. Chay lai...\n")

    if not failed:
        print("Khong co function nao can chay lai.")
        return

    updated_by_id = {r["function_id"]: r for r in log_rows}

    for i, row in enumerate(failed, 1):
        fid = row["function_id"]
        module_name = row["module_name"]
        print(f"[{i}/{len(failed)}] {fid} ({module_name})...", end=" ", flush=True)

        outcome = run_one(module_name)
        status = "OK" if outcome["return_code"] == 0 and outcome["test_file_generated"] else "FAIL"
        print(f"{status} ({outcome['elapsed_seconds']}s)")

        updated_by_id[fid] = {
            "function_id": fid,
            "module_name": module_name,
            "cc_band": row.get("cc_band", ""),
            "cc_value": row.get("cc_value", ""),
            **outcome,
        }

        # Save incrementally
        with open(LOG_PATH, "w", newline="", encoding="utf-8") as f:
            fieldnames = ["function_id", "module_name", "cc_band", "cc_value",
                          "return_code", "elapsed_seconds", "test_file_generated",
                          "stderr_tail", "stdout_tail"]
            writer = csv.DictWriter(f, fieldnames=fieldnames)
            writer.writeheader()
            for fid_key in manifest_by_id:
                if fid_key in updated_by_id:
                    writer.writerow({k: updated_by_id[fid_key].get(k, "") for k in fieldnames})

    n_ok = sum(1 for r in updated_by_id.values() if r["test_file_generated"] in (True, "True"))
    print(f"\n=== HOAN TAT RETRY ===")
    print(f"Tong so OK sau retry: {n_ok}/{len(updated_by_id)}")
    still_failed = [r for r in updated_by_id.values() if r["test_file_generated"] not in (True, "True")]
    if still_failed:
        print(f"\nVAN CON {len(still_failed)} function fail sau retry:")
        for r in still_failed:
            print(f"\n--- {r['function_id']} ---")
            print(f"return_code: {r.get('return_code')}")
            print(f"stdout (cuoi): {r.get('stdout_tail', '')[-400:]}")
            print(f"stderr (cuoi): {r.get('stderr_tail', '')[-400:]}")


if __name__ == "__main__":
    main()
