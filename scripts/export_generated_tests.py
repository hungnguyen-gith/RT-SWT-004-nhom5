import pandas as pd
from pathlib import Path


INPUT = "data/results/llm_output.csv"
OUTPUT_DIR = Path("generated_tests")

OUTPUT_DIR.mkdir(exist_ok=True)


def clean_code(code):

    code = code.replace("```python", "")
    code = code.replace("```", "")

    return code.strip()


df = pd.read_csv(INPUT)


for _, row in df.iterrows():

    function_id = row["function_id"]

    test_code = clean_code(
        row["generated_test"]
    )

    file_path = OUTPUT_DIR / f"{function_id}_test.py"

    with open(
        file_path,
        "w",
        encoding="utf-8"
    ) as f:
        f.write(test_code)

    print("Created:", file_path)


print("DONE")