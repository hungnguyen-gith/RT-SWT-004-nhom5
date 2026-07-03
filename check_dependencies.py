"""
Quet toan bo functions/*.py de tim undefined names (F821) - dau hieu
external dependency chua duoc loai bo theo spec Buoc 2.

Yeu cau: pip install pyflakes (trong pynguin_env)

Usage:
    python check_dependencies.py
"""
import subprocess
import sys
from pathlib import Path

FUNCTIONS_DIR = Path("functions")
REPORT_PATH = Path("data") / "dependency_check_report.txt"


def main():
    py_files = sorted(FUNCTIONS_DIR.glob("*.py"))
    py_files = [f for f in py_files if f.name != "__init__.py"]

    if not py_files:
        print(f"Khong tim thay file .py nao trong {FUNCTIONS_DIR}/")
        sys.exit(1)

    flagged = {}

    for f in py_files:
        result = subprocess.run(
            [sys.executable, "-m", "pyflakes", str(f)],
            capture_output=True, text=True
        )
        output = result.stdout.strip()
        if output:
            # Only care about "undefined name" (F821); ignore unused-import etc.
            undefined_lines = [
                line for line in output.splitlines()
                if "undefined name" in line
            ]
            if undefined_lines:
                flagged[f.name] = undefined_lines

    with open(REPORT_PATH, "w", encoding="utf-8") as out:
        if not flagged:
            out.write("Khong phat hien undefined name nao. Tat ca function OK.\n")
        else:
            out.write(f"Phat hien {len(flagged)}/{len(py_files)} function co undefined name (external dependency):\n\n")
            for fname, lines in flagged.items():
                out.write(f"=== {fname} ===\n")
                for line in lines:
                    out.write(f"  {line}\n")
                out.write("\n")

    print(f"Da quet {len(py_files)} function.")
    print(f"So function bi flag: {len(flagged)}")
    print(f"Chi tiet: {REPORT_PATH}")
    if flagged:
        print("\nDanh sach function bi flag:")
        for fname in flagged:
            print(f"  - {fname}")


if __name__ == "__main__":
    main()
