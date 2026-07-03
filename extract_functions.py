"""
Extract each function from data/full_ground_truth.csv into its own
importable .py file under functions/, ready for Pynguin.

Usage (inside pynguin_env venv, Python 3.10):
    python extract_functions.py
"""
import csv
import re
import sys
from pathlib import Path

CSV_PATH = Path("data/full_ground_truth.csv")
OUT_DIR = Path("functions")


def sanitize_module_name(function_id: str) -> str:
    """PY-001 -> PY_001 (valid Python module/identifier name)."""
    name = re.sub(r"[^0-9a-zA-Z_]", "_", function_id)
    if name[0].isdigit():
        name = "f_" + name
    return name


def main():
    if not CSV_PATH.exists():
        print(f"ERROR: khong tim thay {CSV_PATH}. Chay script nay tu thu muc chua file CSV nay (kiem tra lai cwd bang lenh 'cd').")
        sys.exit(1)

    OUT_DIR.mkdir(exist_ok=True)
    # __init__.py so functions/ is a proper package
    (OUT_DIR / "__init__.py").touch()

    manifest = []
    skipped = []

    with open(CSV_PATH, newline="", encoding="utf-8") as f:
        reader = csv.DictReader(f)
        for row in reader:
            fid = row["function_id"].strip()
            code = row["source_code"]
            module_name = sanitize_module_name(fid)
            out_path = OUT_DIR / f"{module_name}.py"

            try:
                compile(code, str(out_path), "exec")
            except SyntaxError as e:
                skipped.append((fid, str(e)))
                continue

            out_path.write_text(code, encoding="utf-8")
            manifest.append({
                "function_id": fid,
                "module_name": module_name,
                "cc_band": row.get("cc_band", ""),
                "cc_value": row.get("cc_value", ""),
                "file": str(out_path),
            })

    # Write manifest for downstream batch scripts (Pynguin + GPT-4o mini runner)
    manifest_path = Path("data") / "functions_manifest.csv"
    with open(manifest_path, "w", newline="", encoding="utf-8") as f:
        writer = csv.DictWriter(f, fieldnames=["function_id", "module_name", "cc_band", "cc_value", "file"])
        writer.writeheader()
        writer.writerows(manifest)

    print(f"Da tach {len(manifest)} functions vao thu muc '{OUT_DIR}/'")
    print(f"Manifest luu tai: {manifest_path}")
    if skipped:
        print(f"\nCANH BAO: {len(skipped)} function bi loi syntax, KHONG duoc tach:")
        for fid, err in skipped:
            print(f"  - {fid}: {err}")


if __name__ == "__main__":
    main()
