"""
Thay the PY-081 (cycle_sort - nghi bug vong lap vo han, Pynguin timeout 2 lan)
bang function moi (trigger, tu py081_replacement_candidate.csv), giu nguyen
function_id = PY-081 va cc_band = CC9-12 (khong doi stratification).

Usage:
    python swap_py081.py
"""
import csv
from datetime import datetime
from pathlib import Path

FULL_CSV = Path("data/full_ground_truth.csv")
CANDIDATE_CSV = Path("data/py081_replacement_candidate.csv")


def main():
    if not FULL_CSV.exists() or not CANDIDATE_CSV.exists():
        print("ERROR: thieu file can thiet. Chay tu thu muc goc project.")
        return

    with open(CANDIDATE_CSV, newline="", encoding="utf-8") as f:
        candidate = list(csv.DictReader(f))[0]

    with open(FULL_CSV, newline="", encoding="utf-8") as f:
        rows = list(csv.DictReader(f))
        fieldnames = list(rows[0].keys())

    replaced = False
    for row in rows:
        if row["function_id"] == "PY-081":
            row["source_code"] = candidate["source_code"]
            row["cc_value"] = candidate["cc_value"]
            row["annotator_dg"] = ""
            row["annotator_rw"] = ""
            row["final_label"] = "PENDING_ANNOTATION"
            row["notes"] = (f"Replaced cycle_sort (infinite-loop hang under Pynguin fuzzing) "
                             f"with {candidate['func_name']} on {datetime.now().strftime('%Y-%m-%d')} "
                             f"(source: {candidate['url']})")
            replaced = True
            break

    if not replaced:
        print("ERROR: khong tim thay PY-081 trong full_ground_truth.csv")
        return

    with open(FULL_CSV, "w", newline="", encoding="utf-8") as f:
        writer = csv.DictWriter(f, fieldnames=fieldnames)
        writer.writeheader()
        writer.writerows(rows)

    print("Da thay PY-081: cycle_sort -> trigger")
    print("\nChay lai:")
    print("  python extract_functions.py   (tu dong ghi de PY_081.py, khong can xoa truoc)")
    print("  python check_dependencies.py")
    print("  python retry_failed_pynguin.py")


if __name__ == "__main__":
    main()
