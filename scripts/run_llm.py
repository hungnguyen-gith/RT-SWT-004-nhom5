import os
from datetime import datetime

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
USAGE_CSV = "data/results/api_usage.csv"


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

    return {
        "generated_test": response.choices[0].message.content,
        "prompt_tokens": response.usage.prompt_tokens,
        "completion_tokens": response.usage.completion_tokens,
        "total_tokens": response.usage.total_tokens,
        "timestamp": datetime.now().isoformat(),
        "model": MODEL
    }


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

        result = generate_test(code)

        results.append({
            "function_id": function_id,
            "file": file_path,
            "generated_test": result["generated_test"],
            "status": "success",
            "model": result["model"],
            "prompt_tokens": result["prompt_tokens"],
            "completion_tokens": result["completion_tokens"],
            "total_tokens": result["total_tokens"],
            "timestamp": result["timestamp"]
        })

    except Exception as e:

        results.append({
            "function_id": function_id,
            "file": file_path,
            "generated_test": "",
            "status": str(e),
            "model": MODEL,
            "prompt_tokens": 0,
            "completion_tokens": 0,
            "total_tokens": 0,
            "timestamp": datetime.now().isoformat()
        })


df_results = pd.DataFrame(results)

df_results.to_csv(
    OUTPUT_CSV,
    index=False,
    encoding="utf-8"
)

usage_df = df_results[
    [
        "function_id",
        "model",
        "prompt_tokens",
        "completion_tokens",
        "total_tokens",
        "timestamp"
    ]
]

usage_df.to_csv(
    USAGE_CSV,
    index=False,
    encoding="utf-8"
)

print("\n==========================")
print("DONE")
print("Saved:", OUTPUT_CSV)
print("Saved:", USAGE_CSV)

print("\n========== TOKEN SUMMARY ==========")
print("Prompt Tokens     :", usage_df["prompt_tokens"].sum())
print("Completion Tokens :", usage_df["completion_tokens"].sum())
print("Total Tokens      :", usage_df["total_tokens"].sum())
print("===================================")