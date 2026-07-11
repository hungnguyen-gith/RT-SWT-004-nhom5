"""
Tim va thay the 11 function co CC thuc te ngoai khoang 5-15 (phat hien boi
recompute_cc.py / QA review cua RW). Mine function moi tu CodeXGLUE, dam
bao: CC dung band can, tu-chua, ASCII, KHONG bat dau bang "_" (bai hoc tu
loi Pynguin truoc do), khong trung voi dataset hien co.

Ket qua: giu nguyen 11 function_id cu (PY-005, PY-006, ...) nhung THAY
TOAN BO source_code + cc_value + cc_band bang function moi.

Usage:
    python fix_out_of_range_cc.py
"""
import ast
import csv
import gzip
import hashlib
import io
import json
import random
import sys
from collections import Counter
from datetime import datetime
from pathlib import Path

from radon.complexity import cc_visit
from pyflakes.api import check as pyflakes_check
from pyflakes.reporter import Reporter

TRAIN_DIR = Path("data/raw/python/final/jsonl/train")
FULL_CSV = Path("data/full_ground_truth.csv")
SEED = 42

# function_id can thay -> band muc tieu (dua tren CC thuc te ngoai khoang)
TO_REPLACE = {
    "PY-005": "CC5-8",
    "PY-006": "CC5-8",
    "PY-007": "CC5-8",
    "PY-008": "CC5-8",
    "PY-009": "CC5-8",
    "PY-025": "CC9-12",
    "PY-028": "CC9-12",
    "PY-016": "CC9-12",
    "PY-037": "CC13-15",
    "PY-048": "CC13-15",
    "PY-043": "CC9-12",
}
# Phan bo can: CC5-8=5, CC9-12=4, CC13-15=2 (khop voi so luong o tren)

CC_BAND_RANGES = {"CC5-8": (5, 8), "CC9-12": (9, 12), "CC13-15": (13, 15)}
MIN_SLOC = 5

random.seed(SEED)


def cc_band_for(value: int):
    for band, (lo, hi) in CC_BAND_RANGES.items():
        if lo <= value <= hi:
            return band
    return None


def sloc(code: str) -> int:
    return len([l for l in code.splitlines() if l.strip() and not l.strip().startswith("#")])


def is_self_contained(code: str) -> bool:
    buf_out, buf_err = io.StringIO(), io.StringIO()
    pyflakes_check(code, "candidate.py", Reporter(buf_out, buf_err))
    return "undefined name" not in buf_out.getvalue()


def top_level_func_name(code: str):
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
        rows = list(csv.DictReader(f))
        fieldnames = list(rows[0].keys())

    existing_hashes = {normalize_hash(r["source_code"]) for r in rows}
    print(f"Da nap {len(existing_hashes)} function hien co de dedupe.")

    needed = Counter(TO_REPLACE.values())
    print(f"Can tim: {dict(needed)}")

    found = {fid: None for fid in TO_REPLACE}
    remaining_needed = dict(needed)

    shard_files = sorted(TRAIN_DIR.glob("*.jsonl.gz"))
    scanned = 0

    for shard in shard_files:
        with gzip.open(shard, "rt", encoding="utf-8") as f:
            for line in f:
                scanned += 1
                if scanned % 20000 == 0:
                    print(f"  ...da quet {scanned} function, con thieu: {remaining_needed}")

                if not any(v > 0 for v in remaining_needed.values()):
                    break

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

                func_name = top_level_func_name(code)
                if func_name is None or func_name.startswith("_"):
                    continue  # Pynguin bo qua private function

                cc = get_cc(code)
                if cc is None:
                    continue
                band = cc_band_for(cc)
                if band is None or remaining_needed.get(band, 0) <= 0:
                    continue

                if not is_self_contained(code):
                    continue

                # gan cho function_id dau tien con thieu band nay
                target_fid = next(fid for fid, b in TO_REPLACE.items() if b == band and found[fid] is None)
                found[target_fid] = {
                    "cc_value": cc, "func_name": func_name, "url": row.get("url", ""), "source_code": code,
                }
                existing_hashes.add(h)
                remaining_needed[band] -= 1
                print(f"  Tim thay cho {target_fid} ({band}): {func_name}, CC={cc}")
            else:
                # inner for-loop finished without exhausting all quotas -> keep scanning next shard
                continue
        # inner for-loop hit the "break" above (all quotas filled) -> stop scanning shards entirely
        break

    still_missing = [fid for fid, v in found.items() if v is None]
    if still_missing:
        print(f"\nCANH BAO: khong tim du ung vien cho: {still_missing}")
        print("Chay lai script (co the can quet nhieu function hon).")

    # Patch CSV
    timestamp = datetime.now().strftime("%Y-%m-%d")
    n_patched = 0
    for row in rows:
        fid = row["function_id"]
        if fid in found and found[fid] is not None:
            c = found[fid]
            row["source_code"] = c["source_code"]
            row["cc_value"] = str(c["cc_value"])
            row["cc_band"] = TO_REPLACE[fid]
            row["annotator_dg"] = ""
            row["annotator_rw"] = ""
            row["final_label"] = "PENDING_ANNOTATION"
            row["notes"] = (f"Replaced (original CC computed on class/file, not isolated "
                             f"function - QA finding {timestamp}) with {c['func_name']} "
                             f"(source: {c['url']})")
            n_patched += 1

    with open(FULL_CSV, "w", newline="", encoding="utf-8") as f:
        writer = csv.DictWriter(f, fieldnames=fieldnames)
        writer.writeheader()
        writer.writerows(rows)

    print(f"\nDa patch {n_patched}/{len(TO_REPLACE)} function trong {FULL_CSV}")

    band_counts = Counter(r["cc_band"] for r in rows)
    print(f"Phan bo CC band sau khi patch: {dict(band_counts)}")
    target = {"CC5-8": 20, "CC9-12": 20, "CC13-15": 10}
    if band_counts == target:
        print("OK - dung 20/20/10.")
    else:
        print(f"CANH BAO: chua khop target {target}")

    print("\nChay lai:")
    print("  python scripts\\dataset_prep\\extract_functions.py")
    print("  python scripts\\dataset_prep\\check_dependencies.py")
    print("  python recompute_cc.py   (xac nhan khong con lech)")
    print(f"  Chay Pynguin rieng cho {n_patched} function moi (dung "
          f"retry_failed_pynguin.py sau khi xoa dong log cu cua chung, "
          f"hoac chay run_pynguin_batch.py lai toan bo cho chac)")


if __name__ == "__main__":
    main()
