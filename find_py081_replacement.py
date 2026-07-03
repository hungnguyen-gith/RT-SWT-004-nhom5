"""
Tim 1 function CC9-12 thay the cho PY-081 (cycle_sort - nghi co bug vong
lap vo han khien Pynguin treo). Dieu kien giong mine_replacement_functions.py:
tu-chua, ASCII, khong bat dau bang "_" (Pynguin bo qua private function).

Usage:
    python find_py081_replacement.py
"""
import ast
import csv
import gzip
import hashlib
import io
import json
import sys
from pathlib import Path

from radon.complexity import cc_visit
from pyflakes.api import check as pyflakes_check
from pyflakes.reporter import Reporter

TRAIN_DIR = Path("data/raw/python/final/jsonl/train")
FULL_CSV = Path("data/full_ground_truth.csv")
OUTPUT_CSV = Path("data/py081_replacement_candidate.csv")

MIN_SLOC = 5


def sloc(code: str) -> int:
    return len([l for l in code.splitlines() if l.strip() and not l.strip().startswith("#")])


def is_self_contained(code: str) -> bool:
    buf_out, buf_err = io.StringIO(), io.StringIO()
    pyflakes_check(code, "candidate.py", Reporter(buf_out, buf_err))
    return "undefined name" not in buf_out.getvalue()


def is_single_top_level_function(code: str):
    try:
        tree = ast.parse(code)
    except SyntaxError:
        return None
    top_defs = [n for n in tree.body if isinstance(n, ast.FunctionDef)]
    other = [n for n in tree.body if not isinstance(n, (ast.FunctionDef, ast.Import, ast.ImportFrom))]
    if len(top_defs) == 1 and len(other) == 0:
        return top_defs[0].name
    return None


def get_cc(code: str):
    try:
        blocks = cc_visit(code)
    except Exception:
        return None
    return blocks[0].complexity if blocks else None


def normalize_hash(code: str) -> str:
    return hashlib.sha256("".join(code.split()).encode("utf-8")).hexdigest()


def main():
    if not TRAIN_DIR.exists():
        print(f"ERROR: khong tim thay {TRAIN_DIR}")
        sys.exit(1)

    with open(FULL_CSV, newline="", encoding="utf-8") as f:
        existing = list(csv.DictReader(f))
    existing_hashes = {normalize_hash(r["source_code"]) for r in existing}
    print(f"Da nap {len(existing_hashes)} function hien co de dedupe.")

    shard_files = sorted(TRAIN_DIR.glob("*.jsonl.gz"))
    scanned = 0

    for shard in shard_files:
        with gzip.open(shard, "rt", encoding="utf-8") as f:
            for line in f:
                scanned += 1
                if scanned % 20000 == 0:
                    print(f"  ...da quet {scanned} function")
                try:
                    row = json.loads(line)
                except json.JSONDecodeError:
                    continue

                code = row.get("code", "")
                if not code or sloc(code) < MIN_SLOC or not code.isascii():
                    continue

                h = normalize_hash(code)
                if h in existing_hashes:
                    continue

                func_name = is_single_top_level_function(code)
                if func_name is None or func_name.startswith("_"):
                    continue  # skip private functions - Pynguin ignores them

                cc = get_cc(code)
                if cc is None or not (9 <= cc <= 12):
                    continue

                if not is_self_contained(code):
                    continue

                # avoid another sorting/searching algorithm with loop patterns similar to cycle_sort
                if "cycle_sort" in code.lower() or "while" in code and code.count("while") >= 2:
                    continue  # be conservative: skip functions with multiple while-loops (higher hang risk)

                with open(OUTPUT_CSV, "w", newline="", encoding="utf-8") as out:
                    writer = csv.DictWriter(out, fieldnames=["function_id", "language", "cc_band", "cc_value", "func_name", "url", "source_code"])
                    writer.writeheader()
                    writer.writerow({
                        "function_id": "PY-081",
                        "language": "python",
                        "cc_band": "CC9-12",
                        "cc_value": cc,
                        "func_name": func_name,
                        "url": row.get("url", ""),
                        "source_code": code,
                    })
                print(f"\nDa tim thay ung vien sau khi quet {scanned} function:")
                print(f"  func_name: {func_name}")
                print(f"  cc_value: {cc}")
                print(f"  url: {row.get('url', '')}")
                print(f"Da luu vao: {OUTPUT_CSV}")
                return

    print("Khong tim duoc ung vien phu hop trong toan bo dataset da quet.")


if __name__ == "__main__":
    main()
