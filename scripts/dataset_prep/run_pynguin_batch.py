"""
Chay Pynguin (DYNAMOSA, seed=42, 60s/function) qua toan bo 50 function
trong data/functions_manifest.csv. Luu test suite vao baseline/pynguin_tests/
va log ket qua tung function vao data/results/pynguin_batch_log.csv.

Thoi gian du kien: 50 function x toi da 60s = ~50 phut (co the nhanh hon
neu Pynguin hoi tu som).

Usage:
    python run_pynguin_batch.py
"""
import csv
import os
import subprocess
import sys
import time
from pathlib import Path

MANIFEST = Path("data/functions_manifest.csv")
PROJECT_PATH = Path("functions")
OUTPUT_PATH = Path("baseline/pynguin_tests")
LOG_PATH = Path("data/results/pynguin_batch_log.csv")
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
            "stderr_tail": result.stderr[-500:] if result.returncode != 0 else "",
        }
    except subprocess.TimeoutExpired:
        elapsed = time.time() - start
        return {
            "return_code": -1,
            "elapsed_seconds": round(elapsed, 1),
            "test_file_generated": False,
            "stderr_tail": "TIMEOUT - Pynguin khong hoan thanh trong thoi gian cho phep",
        }


def main():
    if not MANIFEST.exists():
        print(f"ERROR: khong tim thay {MANIFEST}")
        sys.exit(1)

    OUTPUT_PATH.mkdir(parents=True, exist_ok=True)
    LOG_PATH.parent.mkdir(parents=True, exist_ok=True)

    with open(MANIFEST, newline="", encoding="utf-8") as f:
        manifest_rows = list(csv.DictReader(f))

    print(f"Chuan bi chay Pynguin qua {len(manifest_rows)} function.")
    print(f"Algorithm={ALGORITHM}, seed={SEED}, max-search-time={MAX_SEARCH_TIME}s/function")
    print(f"Uoc tinh toi da: {len(manifest_rows) * MAX_SEARCH_TIME / 60:.0f} phut\n")

    log_rows = []
    for i, row in enumerate(manifest_rows, 1):
        module_name = row["module_name"]
        function_id = row["function_id"]
        print(f"[{i}/{len(manifest_rows)}] {function_id} ({module_name})...", end=" ", flush=True)

        outcome = run_one(module_name)
        status = "OK" if outcome["return_code"] == 0 and outcome["test_file_generated"] else "FAIL"
        print(f"{status} ({outcome['elapsed_seconds']}s)")

        log_rows.append({
            "function_id": function_id,
            "module_name": module_name,
            "cc_band": row.get("cc_band", ""),
            "cc_value": row.get("cc_value", ""),
            **outcome,
        })

        # Write log incrementally so partial progress isn't lost if interrupted
        with open(LOG_PATH, "w", newline="", encoding="utf-8") as f:
            fieldnames = ["function_id", "module_name", "cc_band", "cc_value",
                          "return_code", "elapsed_seconds", "test_file_generated", "stderr_tail"]
            writer = csv.DictWriter(f, fieldnames=fieldnames)
            writer.writeheader()
            writer.writerows(log_rows)

    n_ok = sum(1 for r in log_rows if r["test_file_generated"])
    n_fail = len(log_rows) - n_ok
    print(f"\n=== HOAN TAT ===")
    print(f"Thanh cong: {n_ok}/{len(log_rows)}")
    print(f"That bai: {n_fail}/{len(log_rows)}")
    print(f"Log chi tiet: {LOG_PATH}")
    print(f"Test suite: {OUTPUT_PATH}/")
    if n_fail:
        print("\nCac function that bai:")
        for r in log_rows:
            if not r["test_file_generated"]:
                print(f"  - {r['function_id']} ({r['module_name']}): {r['stderr_tail'][:150]}")


if __name__ == "__main__":
    main()
