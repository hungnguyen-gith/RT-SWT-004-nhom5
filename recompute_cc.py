"""
Tinh lai CC THUC SU cho ca 50 function (tren source code da tach rieng,
khong con nam trong class/file goc), doi chieu voi cc_value dang luu trong
full_ground_truth.csv, va tu dong cap nhat neu sai lech.

CANH BAO: neu CC thuc te ra ngoai khoang 5-15, function do VI PHAM tieu chi
loc co ban (Buoc 2) va can duoc THAY THE, khong chi sua so.

Usage:
    python recompute_cc.py
"""
import csv
from pathlib import Path

from radon.complexity import cc_visit

FULL_CSV = Path("data/full_ground_truth.csv")
REPORT_PATH = Path("data/archive/cc_recompute_report.txt")


def cc_band_for(value: int):
    if 5 <= value <= 8:
        return "CC5-8"
    if 9 <= value <= 12:
        return "CC9-12"
    if 13 <= value <= 15:
        return "CC13-15"
    return None  # ngoai khoang hop le


def get_actual_cc(code: str):
    try:
        blocks = cc_visit(code)
    except Exception as e:
        return None, str(e)
    if not blocks:
        return None, "khong tim thay function nao"
    return blocks[0].complexity, None


def main():
    with open(FULL_CSV, newline="", encoding="utf-8") as f:
        rows = list(csv.DictReader(f))
        fieldnames = list(rows[0].keys())

    mismatches = []
    out_of_range = []

    for row in rows:
        expected = int(row["cc_value"])
        actual, err = get_actual_cc(row["source_code"])

        if actual is None:
            mismatches.append((row["function_id"], expected, f"ERROR: {err}"))
            continue

        if actual != expected:
            mismatches.append((row["function_id"], expected, actual))
            row["cc_value"] = str(actual)
            new_band = cc_band_for(actual)
            if new_band is None:
                out_of_range.append((row["function_id"], actual))
            else:
                row["cc_band"] = new_band

    with open(FULL_CSV, "w", newline="", encoding="utf-8") as f:
        writer = csv.DictWriter(f, fieldnames=fieldnames)
        writer.writeheader()
        writer.writerows(rows)

    with open(REPORT_PATH, "w", encoding="utf-8") as f:
        f.write(f"Kiem tra {len(rows)} function.\n")
        f.write(f"So function bi lech CC: {len(mismatches)}\n\n")
        for fid, exp, act in mismatches:
            f.write(f"  {fid}: ky vong {exp}, thuc te {act}\n")
        f.write(f"\nSo function co CC NGOAI KHOANG 5-15 sau khi tinh lai: {len(out_of_range)}\n")
        for fid, act in out_of_range:
            f.write(f"  {fid}: CC thuc te = {act} (VI PHAM tieu chi loc, can THAY THE)\n")

    print(f"Da kiem tra {len(rows)} function.")
    print(f"So function bi lech CC (da tu dong sua trong CSV): {len(mismatches)}")
    for fid, exp, act in mismatches:
        print(f"  {fid}: ky vong {exp} -> thuc te {act}")

    if out_of_range:
        print(f"\nCANH BAO: {len(out_of_range)} function co CC ngoai khoang 5-15 sau khi tinh lai:")
        for fid, act in out_of_range:
            print(f"  {fid}: CC={act} -> VI PHAM, CAN THAY THE (khong chi sua so)")

    # Verify final stratification
    from collections import Counter
    band_counts = Counter(r["cc_band"] for r in rows if cc_band_for(int(r["cc_value"])) is not None)
    print(f"\nPhan bo CC band sau khi cap nhat: {dict(band_counts)}")
    print(f"Report chi tiet: {REPORT_PATH}")


if __name__ == "__main__":
    main()
