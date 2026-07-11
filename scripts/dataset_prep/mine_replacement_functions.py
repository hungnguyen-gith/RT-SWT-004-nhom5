"""
Mine replacement functions tu CodeXGLUE/CodeSearchNet python train shards.

Yeu cau:
    pip install radon pyflakes

Muc tieu: tim 9 function CC5-8 + 9 function CC9-12, tu-chua (khong external
dependency), thay the cho 16 function bi loai (Group B) + 2 function CC13-15
du ra, de dat dung stratification 20/20/10.

Usage:
    python mine_replacement_functions.py
"""
import ast
import csv
import gzip
import hashlib
import io
import json
import random
import sys
from pathlib import Path

from radon.complexity import cc_visit
from pyflakes.api import check as pyflakes_check
from pyflakes.reporter import Reporter

TRAIN_DIR = Path("data/raw/python/final/jsonl/train")
EXISTING_CSV = Path("data/full_ground_truth.csv")
OUTPUT_CSV = Path("data/replacement_candidates.csv")

NEEDED = {"CC5-8": 9, "CC9-12": 9}
CC_BAND_RANGES = {"CC5-8": (5, 8), "CC9-12": (9, 12)}
MIN_SLOC = 5
SEED = 42

random.seed(SEED)


def cc_band_for(value: int):
    for band, (lo, hi) in CC_BAND_RANGES.items():
        if lo <= value <= hi:
            return band
    return None


def sloc(code: str) -> int:
    lines = [l for l in code.splitlines() if l.strip() and not l.strip().startswith("#")]
    return len(lines)


def is_self_contained(code: str) -> bool:
    """Return True if pyflakes finds zero 'undefined name' warnings."""
    buf_out, buf_err = io.StringIO(), io.StringIO()
    reporter = Reporter(buf_out, buf_err)
    pyflakes_check(code, "candidate.py", reporter)
    output = buf_out.getvalue()
    return "undefined name" not in output


def is_ascii_only(code: str) -> bool:
    """Reject candidates with non-ASCII characters (e.g. CJK docstrings/comments)
    to keep the dataset language-consistent with the rest of the corpus."""
    return code.isascii()


def is_single_top_level_function(code: str) -> bool:
    try:
        tree = ast.parse(code)
    except SyntaxError:
        return False
    top_defs = [n for n in tree.body if isinstance(n, ast.FunctionDef)]
    other = [n for n in tree.body if not isinstance(n, (ast.FunctionDef, ast.Import, ast.ImportFrom))]
    return len(top_defs) == 1 and len(other) == 0


def get_cc(code: str):
    try:
        blocks = cc_visit(code)
    except Exception:
        return None
    if not blocks:
        return None
    # single top-level function -> take its complexity
    return blocks[0].complexity


def normalize_hash(code: str) -> str:
    normalized = "".join(code.split())
    return hashlib.sha256(normalized.encode("utf-8")).hexdigest()


def load_existing_hashes():
    hashes = set()
    if not EXISTING_CSV.exists():
        return hashes
    with open(EXISTING_CSV, newline="", encoding="utf-8") as f:
        reader = csv.DictReader(f)
        for row in reader:
            hashes.add(normalize_hash(row["source_code"]))
    return hashes


def main():
    if not TRAIN_DIR.exists():
        print(f"ERROR: khong tim thay {TRAIN_DIR}")
        sys.exit(1)

    existing_hashes = load_existing_hashes()
    print(f"Da nap {len(existing_hashes)} function hien co de dedupe.")

    candidates = {"CC5-8": [], "CC9-12": []}
    seen_hashes = set(existing_hashes)

    shard_files = sorted(TRAIN_DIR.glob("*.jsonl.gz"))
    print(f"Quet {len(shard_files)} shard...")

    scanned = 0
    for shard in shard_files:
        with gzip.open(shard, "rt", encoding="utf-8") as f:
            for line in f:
                scanned += 1
                if scanned % 20000 == 0:
                    print(f"  ...da quet {scanned} function, tim duoc "
                          f"{len(candidates['CC5-8'])} CC5-8, {len(candidates['CC9-12'])} CC9-12")

                # Early stop once both quotas comfortably exceeded (collect 3x buffer for manual review)
                if len(candidates["CC5-8"]) >= NEEDED["CC5-8"] * 3 and \
                   len(candidates["CC9-12"]) >= NEEDED["CC9-12"] * 3:
                    break

                try:
                    row = json.loads(line)
                except json.JSONDecodeError:
                    continue

                code = row.get("code", "")
                if not code or sloc(code) < MIN_SLOC:
                    continue

                h = normalize_hash(code)
                if h in seen_hashes:
                    continue

                if not is_single_top_level_function(code):
                    continue

                cc = get_cc(code)
                if cc is None:
                    continue

                band = cc_band_for(cc)
                if band is None:
                    continue

                if len(candidates[band]) >= NEEDED[band] * 3:
                    continue  # already have enough buffer for this band

                if not is_self_contained(code):
                    continue

                if not is_ascii_only(code):
                    continue

                seen_hashes.add(h)
                candidates[band].append({
                    "url": row.get("url", ""),
                    "func_name": row.get("func_name", ""),
                    "cc_band": band,
                    "cc_value": cc,
                    "sloc": sloc(code),
                    "source_code": code,
                })
            else:
                # inner for-loop finished without hitting quota break -> keep scanning next shard
                continue
        # inner for-loop hit the quota break -> stop scanning shards entirely
        break

    print(f"\nTong cong da quet {scanned} function.")
    print(f"Ung vien tim duoc: CC5-8={len(candidates['CC5-8'])}, CC9-12={len(candidates['CC9-12'])}")

    # Sample final selection (with buffer, pick first N after shuffle for reproducibility)
    final_rows = []
    next_id = 66  # continue from PY-066
    for band, need in NEEDED.items():
        pool = candidates[band]
        random.shuffle(pool)
        if len(pool) < need:
            print(f"CANH BAO: chi tim duoc {len(pool)}/{need} ung vien cho {band}!")
        selected = pool[:need]
        for item in selected:
            item["function_id"] = f"PY-{next_id:03d}"
            item["language"] = "python"
            next_id += 1
            final_rows.append(item)

    with open(OUTPUT_CSV, "w", newline="", encoding="utf-8") as f:
        fieldnames = ["function_id", "language", "cc_band", "cc_value", "sloc", "func_name", "url", "source_code"]
        writer = csv.DictWriter(f, fieldnames=fieldnames)
        writer.writeheader()
        for row in final_rows:
            writer.writerow({k: row.get(k, "") for k in fieldnames})

    print(f"\nDa luu {len(final_rows)} function thay the vao: {OUTPUT_CSV}")
    print("XEM LAI THU CONG truoc khi merge vao full_ground_truth.csv "
          "(kiem tra docstring/code khong chua noi dung nhay cam, license phu hop).")


if __name__ == "__main__":
    main()
