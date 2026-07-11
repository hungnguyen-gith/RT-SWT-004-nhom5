from openai import OpenAI
from dotenv import load_dotenv
import os

load_dotenv()

key = os.getenv("OPENAI_API_KEY")

print("API key loaded:", key[:8] if key else "NOT FOUND")

client = OpenAI(
    api_key=key
)

response = client.chat.completions.create(
    model="gpt-4o-mini-2024-07-18",
    temperature=0,
    messages=[
        {
            "role": "user",
            "content": "Reply only: GPT-4o mini is working"
        }
    ]
)

print(response.choices[0].message.content)