import subprocess
from pathlib import Path
import pandas as pd


TEST_DIR = Path("generated_tests")
OUTPUT = "data/results/csr_report.csv"


results = []


for test_file in TEST_DIR.glob("*_test.py"):

    print("Checking:", test_file.name)

    try:
        result = subprocess.run(
            [
                "python",
                "-m",
                "py_compile",
                str(test_file)
            ],
            capture_output=True,
            text=True
        )

        success = result.returncode == 0

        results.append({
            "test_file": test_file.name,
            "compile_success": int(success),
            "error": result.stderr if not success else ""
        })


    except Exception as e:

        results.append({
            "test_file": test_file.name,
            "compile_success": 0,
            "error": str(e)
        })


df = pd.DataFrame(results)

df.to_csv(
    OUTPUT,
    index=False
)


print("===================")
print(df["compile_success"].value_counts())

csr = df["compile_success"].mean()

print("CSR =", csr)
print("===================")