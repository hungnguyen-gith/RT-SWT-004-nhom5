#!/usr/bin/env python3
"""
test_api.py — Gate E3: kiem tra API hoat dong dung voi 1 call truoc khi chay batch
Du an: Evaluating GPT-4o mini Zero-Shot for Unit Test Generation (Nhom 5)

CACH DUNG
---------
    export OPENAI_API_KEY=sk-...
    python scripts/test_api.py
    python scripts/test_api.py --function-id PY-003 --input data/pilot_sample.csv
"""

import argparse
import os
import sys
import time

import pandas as pd

try:
    from openai import OpenAI
except ImportError:
    print("Chua cai package 'openai'. Chay: pip install openai --break-system-packages", file=sys.stderr)
    sys.exit(1)

PRICE_PER_1M_INPUT = 0.15
PRICE_PER_1M_OUTPUT = 0.60

ZERO_SHOT_PROMPT_TEMPLATE = """You are a Python testing expert. Write pytest unit tests for the function below.
Requirements:
- Use pytest (not unittest)
- Cover normal cases, edge cases, and invalid input where applicable
- Output ONLY valid Python code (the test file content), no explanation, no markdown fences

Function to test:
```python
{source_code}
```
"""


def build_prompt(source_code: str) -> str:
    return ZERO_SHOT_PROMPT_TEMPLATE.format(source_code=source_code)


def load_one_function(csv_path: str, function_id):
    if not os.path.exists(csv_path):
        print(f"Khong tim thay file: {csv_path}", file=sys.stderr)