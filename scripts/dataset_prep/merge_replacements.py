"""
Merge cuoi cung: xay dung lai full_ground_truth.csv dat N=50 dung chuan:
- Loai 16 function Group B (vi pham "no external dependency")
- Loai 2 function CC13-15 du ra (khong thuoc pilot IAA, an toan de loai)
- Them 18 function thay the (9 CC5-8 + 9 CC9-12) tu replacement_candidates.csv
- Ket qua cuoi: CC5-8=20, CC9-12=20, CC13-15=10 (dung 40/40/20%)

18 function moi CHUA co nhan Maintainable/Hard (annotator_dg, annotator_rw,
final_label de trong, notes ghi "PENDING_ANNOTATION") - can gan nhan thu cong
+ chay lai calculate_iaa.py sau, giong quy trinh da lam cho 32 function con lai.

Usage:
    python merge_replacements.py
"""
import csv
import random
import shutil
from datetime import datetime
from pathlib import Path

FULL_CSV = Path("data/full_ground_truth.csv")
CANDIDATES_CSV = Path("data/replacement_candidates.csv")
SEED = 42

GROUP_B_IDS = {
    "PY-001", "PY-002", "PY-003", "PY-004", "PY-010", "PY-012", "PY-013",
    "PY-017", "PY-018", "PY-019", "PY-022", "PY-026", "PY-027", "PY-029",
    "PY-040", "PY-041",
}

# function_ids used in pilot IAA phase - never drop these even if in the
# "excess CC13-15" trim step, to avoid invalidating already-completed IAA work
PILOT_IDS = {"PY-001", "PY-002", "PY-003", "PY-004", "PY-008", "PY-011", "PY-015", "PY-019", "PY-049", "PY-054"}

FIELDNAMES = ["function_id", "language", "cc_band", "cc_value", "source_code",
              "annotator_dg", "annotator_rw", "final_label", "notes"]


def main():
    if not FULL_CSV.exists() or not CANDIDATES_CSV.exists():
        print(f"ERROR: can ca {FULL_CSV} va {CANDIDATES_CSV}. Chay tu thu muc goc project.")
        return

    # 1. Backup
    timestamp = datetime.now().strftime("%Y%m%d_%H%M%S")
    backup_path = FULL_CSV.with_name(f"full_ground_truth_backup_{timestamp}.csv")
    shutil.copy(FULL_CSV, backup_path)
    print(f"Da backup file goc vao: {backup_path}")

    # 2. Load existing
    with open(FULL_CSV, newline="", encoding="utf-8") as f:
        rows = list(csv.DictReader(f))
    print(f"Da nap {len(rows)} function hien co.")

    # 3. Remove Group B
    kept = [r for r in rows if r["function_id"] not in GROUP_B_IDS]
    removed_b = len(rows) - len(kept)
    print(f"Da loai {removed_b} function Group B (vi pham external dependency).")

    # 4. Trim 2 excess CC13-15 (never touch pilot IDs)
    cc13_pool = [r for r in kept if r["cc_band"] == "CC13-15" and r["function_id"] not in PILOT_IDS]
    random.seed(SEED)
    random.shuffle(cc13_pool)
    to_drop_ids = {r["function_id"] for r in cc13_pool[:2]}
    kept = [r for r in kept if r["function_id"] not in to_drop_ids]
    print(f"Da loai 2 function CC13-15 du (khong thuoc pilot IAA): {sorted(to_drop_ids)}")

    # 5. Load and append replacements
    with open(CANDIDATES_CSV, newline="", encoding="utf-8") as f:
        candidates = list(csv.DictReader(f))

    new_rows = []
    for c in candidates:
        new_rows.append({
            "function_id": c["function_id"],
            "language": c["language"],
            "cc_band": c["cc_band"],
            "cc_value": c["cc_value"],
            "source_code": c["source_code"],
            "annotator_dg": "",
            "annotator_rw": "",
            "final_label": "PENDING_ANNOTATION",
            "notes": f"Replacement function added {timestamp} (source: {c['url']})",
        })
    print(f"Da them {len(new_rows)} function thay the.")

    final_rows = kept + new_rows
    print(f"\nTong so function sau merge: {len(final_rows)}")

    # 6. Verify stratification
    from collections import Counter
    band_counts = Counter(r["cc_band"] for r in final_rows)
    print(f"Phan bo CC band: {dict(band_counts)}")
    target = {"CC5-8": 20, "CC9-12": 20, "CC13-15": 10}
    if band_counts == target:
        print("OK - dung 20/20/10 nhu spec.")
    else:
        print(f"CANH BAO: khong khop target {target}!")

    # 7. Write output (only known fields; ignore any extra old columns silently)
    with open(FULL_CSV, "w", newline="", encoding="utf-8") as f:
        writer = csv.DictWriter(f, fieldnames=FIELDNAMES)
        writer.writeheader()
        for r in final_rows:
            writer.writerow({k: r.get(k, "") for k in FIELDNAMES})

    print(f"\nDa ghi de: {FULL_CSV}")
    print("\n=== VIEC CAN LAM TIEP ===")
    print("1. Xoa thu muc functions/ cu va chay lai extract_functions.py de tach lai toan bo 50 function.")
    print("2. Chay lai check_dependencies.py de xac nhan KHONG con function nao vi pham.")
    print(f"3. Gan nhan Maintainable/Hard cho 18 function moi ({', '.join(r['function_id'] for r in new_rows)}) "
          f"giong quy trinh da lam cho cac function con lai, roi chay lai calculate_iaa.py.")


if __name__ == "__main__":
    main()
