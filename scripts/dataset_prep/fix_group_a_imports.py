"""
Them import con thieu vao 8 function Nhom A (chi thieu thu vien chuan,
khong phai external dependency thuc su). Patch truc tiep vao
full_ground_truth.csv (nguon su that), sau do can chay lai
extract_functions.py de dong bo functions/.

Usage:
    python fix_group_a_imports.py
"""
import csv
from pathlib import Path

FULL_CSV = Path("data/full_ground_truth.csv")

# function_id (dang PY-XXX trong CSV) -> danh sach dong import can them vao dau ham
IMPORTS_TO_ADD = {
    "PY-009": ["import numpy as np"],
    "PY-011": ["import numpy as np"],
    "PY-025": ["import numpy as np"],
    "PY-042": ["import numpy as np"],
    "PY-048": ["import numpy as np"],
    "PY-021": ["import plotly.graph_objects as go"],
    "PY-020": [
        "import numpy as np",
        "import matplotlib.pyplot as plt",
        "from sklearn.preprocessing import StandardScaler",
        "from sklearn.manifold import TSNE",
    ],
    "PY-023": [
        "import os",
        "import numpy as np",
        "import pandas as pd",
        "import matplotlib.pyplot as plt",
    ],
}


def main():
    if not FULL_CSV.exists():
        print(f"ERROR: khong tim thay {FULL_CSV}")
        return

    with open(FULL_CSV, newline="", encoding="utf-8") as f:
        rows = list(csv.DictReader(f))
        fieldnames = list(rows[0].keys())

    patched = 0
    for row in rows:
        fid = row["function_id"]
        if fid in IMPORTS_TO_ADD:
            imports_block = "\n".join(IMPORTS_TO_ADD[fid])
            row["source_code"] = imports_block + "\n\n\n" + row["source_code"]
            patched += 1
            print(f"Da patch {fid}: +{len(IMPORTS_TO_ADD[fid])} dong import")

    with open(FULL_CSV, "w", newline="", encoding="utf-8") as f:
        writer = csv.DictWriter(f, fieldnames=fieldnames)
        writer.writeheader()
        writer.writerows(rows)

    print(f"\nDa patch {patched}/{len(IMPORTS_TO_ADD)} function.")
    print("Chay lai: Remove-Item functions\\*.py -Exclude __init__.py; python extract_functions.py; python check_dependencies.py")


if __name__ == "__main__":
    main()
