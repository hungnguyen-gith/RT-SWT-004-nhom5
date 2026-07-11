import os
import pandas as pd
from openai import OpenAI
from dotenv import load_dotenv


load_dotenv()

client = OpenAI(
    api_key=os.getenv("OPENAI_API_KEY")
)

MODEL = "gpt-4o-mini-2024-07-18"

INPUT_CSV = "data/functions_manifest.csv"
OUTPUT_CSV = "data/results/llm_output.csv"


def generate_test(source_code):

    prompt = f"""
You are a software testing expert.

Generate pytest unit tests for this Python function.

Requirements:
- Use pytest
- Include normal test cases
- Include boundary test cases
- Include edge cases
- Return ONLY Python test code
- Do not explain

Function:

{source_code}
"""

    response = client.chat.completions.create(
        model=MODEL,
        temperature=0,
        max_tokens=2048,
        messages=[
            {
                "role": "user",
                "content": prompt
            }
        ]
    )

    return response.choices[0].message.content


df = pd.read_csv(INPUT_CSV)

results = []

total = len(df)

for i, row in df.iterrows():

    function_id = row["function_id"]
    file_path = row["file"]

    print(f"[{i+1}/{total}] Generating test for {function_id}")

    with open(file_path, "r", encoding="utf-8") as f:
        code = f.read()


    try:
        test_code = generate_test(code)

        results.append({
            "function_id": function_id,
            "file": file_path,
            "generated_test": test_code,
            "status": "success"
        })

    except Exception as e:

        results.append({
            "function_id": function_id,
            "file": file_path,
            "generated_test": "",
            "status": str(e)
        })


pd.DataFrame(results).to_csv(
    OUTPUT_CSV,
    index=False,
    encoding="utf-8"
)


print("==========================")
print("DONE")
print("Saved:", OUTPUT_CSV)