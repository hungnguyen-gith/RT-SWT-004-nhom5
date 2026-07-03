"""
Fix 2 loai loi Pynguin phat hien:
1. Pynguin bo qua function co ten bat dau bang "_" (coi la private, khong
   phai public API) -> bao "SUT contains nothing we can test".
   Fix: bo dau "_" dau tien trong ten function (chi ten function top-level,
   khong dung cham vao cac ten bien/attribute khac).
2. PY-020 dung matplotlib voi backend GUI (Tk) mac dinh -> crash khi chay
   hang loat khong co man hinh. Fix: ep dung backend 'Agg' (non-GUI).

QUAN TRONG: patch truc tiep vao full_ground_truth.csv (nguon su that),
sau do phai chay lai extract_functions.py de dong bo functions/.

Usage:
    python fix_pynguin_issues.py
"""
import csv
import re
from pathlib import Path

FULL_CSV = Path("data/full_ground_truth.csv")

# function_id -> ten function GOC (co dau _) can doi
UNDERSCORE_FIXES = {
    "PY-008": "_get_BFs",
    "PY-011": "_get_top_cluster_params",
    "PY-067": "_akima_interpolate",
    "PY-068": "_check_is_max_context",
    "PY-069": "_apply_axis_properties",
    "PY-071": "_rehydrate_skeleton_class",
    "PY-073": "_trim_front",
    "PY-074": "_extend_blocks",
    "PY-076": "_preprocess_sgm",
    "PY-082": "_process_nested_expression",
}

MATPLOTLIB_BACKEND_FIX_ID = "PY-020"


def strip_leading_underscore(code: str, old_name: str) -> str:
    new_name = old_name.lstrip("_")
    # Replace only whole-word occurrences of old_name (covers the def line
    # and any recursive/self-referential calls using the bare name)
    pattern = re.compile(r"\b" + re.escape(old_name) + r"\b")
    return pattern.sub(new_name, code)


def fix_matplotlib_backend(code: str) -> str:
    return code.replace(
        "import matplotlib.pyplot as plt",
        "import matplotlib\nmatplotlib.use('Agg')\nimport matplotlib.pyplot as plt",
    )


def main():
    if not FULL_CSV.exists():
        print(f"ERROR: khong tim thay {FULL_CSV}")
        return

    with open(FULL_CSV, newline="", encoding="utf-8") as f:
        rows = list(csv.DictReader(f))
        fieldnames = list(rows[0].keys())

    fixed = []
    for row in rows:
        fid = row["function_id"]
        if fid in UNDERSCORE_FIXES:
            old_name = UNDERSCORE_FIXES[fid]
            row["source_code"] = strip_leading_underscore(row["source_code"], old_name)
            fixed.append(f"{fid}: {old_name} -> {old_name.lstrip('_')}")
        if fid == MATPLOTLIB_BACKEND_FIX_ID:
            if "matplotlib.use" not in row["source_code"]:
                row["source_code"] = fix_matplotlib_backend(row["source_code"])
                fixed.append(f"{fid}: forced matplotlib backend to Agg")

    with open(FULL_CSV, "w", newline="", encoding="utf-8") as f:
        writer = csv.DictWriter(f, fieldnames=fieldnames)
        writer.writeheader()
        writer.writerows(rows)

    print(f"Da fix {len(fixed)} function:")
    for line in fixed:
        print(f"  - {line}")

    print("\nChay lai:")
    print("  Remove-Item functions\\*.py -Exclude __init__.py")
    print("  python extract_functions.py")
    print("  python check_dependencies.py   (phai van ra 0 flag)")
    print("  python retry_failed_pynguin.py")


if __name__ == "__main__":
    main()
