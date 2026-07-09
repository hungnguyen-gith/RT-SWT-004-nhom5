import os
import time
import random
from datetime import datetime

import pandas as pd
from dotenv import load_dotenv
from openai import OpenAI

# ==========================
# Load API
# ==========================

load_dotenv()

client = OpenAI(
    api_key=os.getenv("OPENAI_API_KEY")
)

# ==========================
# Config
# ==========================

MODEL = "gpt-4o-mini-2024-07-18"

INPUT_FILE = "data/full_ground_truth.csv"

OUTPUT_FILE = "results/full_llm_output.csv"

LOG_FILE = "results/full_api_log.txt"

MAX_RETRY = 5

os.makedirs("results", exist_ok=True)

# ==========================
# Read Dataset
# ==========================

df = pd.read_csv(INPUT_FILE)

print("=" * 60)
print(f"Loaded {len(df)} functions")
print("=" * 60)

results = []

# ==========================
# Run Experiment
# ==========================

for index, row in df.iterrows():

    function_id = row["function_id"]

    code = row["source_code"]

    print(f"\nProcessing {index+1}/{len(df)} : {function_id}")

    prompt = f"""
Generate Python pytest unit tests for the following Python function.

Requirements

- Use pytest
- Maximize branch coverage
- Return ONLY Python code
- No explanation
- No markdown

Function

{code}
"""

    success = False

    for retry in range(MAX_RETRY):

        try:

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

            generated_test = response.choices[0].message.content

            usage = response.usage

            prompt_tokens = usage.prompt_tokens

            completion_tokens = usage.completion_tokens

            total_tokens = usage.total_tokens

            timestamp = datetime.now().strftime("%Y-%m-%d %H:%M:%S")

            results.append({

                "function_id": function_id,

                "language": row["language"],

                "cc_band": row["cc_band"],

                "cc_value": row["cc_value"],

                "generated_test": generated_test,

                "prompt_tokens": prompt_tokens,

                "completion_tokens": completion_tokens,

                "total_tokens": total_tokens,

                "timestamp": timestamp

            })

            pd.DataFrame(results).to_csv(
                OUTPUT_FILE,
                index=False
            )

            with open(LOG_FILE, "a", encoding="utf8") as f:

                f.write("=" * 60 + "\n")

                f.write(f"{timestamp}\n")

                f.write(f"{function_id}\n")

                f.write(f"Prompt Tokens : {prompt_tokens}\n")

                f.write(f"Completion Tokens : {completion_tokens}\n")

                f.write(f"Total Tokens : {total_tokens}\n")

                f.write("\n")

            print(f"✓ Done ({total_tokens} tokens)")

            success = True

            break

        except Exception as e:

            print(f"Retry {retry+1}/{MAX_RETRY}")

            print(e)

            wait = 2 ** retry + random.random()

            time.sleep(wait)

    if not success:

        results.append({

            "function_id": function_id,

            "language": row["language"],

            "cc_band": row["cc_band"],

            "cc_value": row["cc_value"],

            "generated_test": "INVALID",

            "prompt_tokens": 0,

            "completion_tokens": 0,

            "total_tokens": 0,

            "timestamp": datetime.now().strftime("%Y-%m-%d %H:%M:%S")

        })

        pd.DataFrame(results).to_csv(
            OUTPUT_FILE,
            index=False
        )

print("\n" + "=" * 60)

print("Experiment Finished")

print(f"Output : {OUTPUT_FILE}")

print(f"Log : {LOG_FILE}")

print("=" * 60)