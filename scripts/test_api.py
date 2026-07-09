from openai import OpenAI
from dotenv import load_dotenv
import os

load_dotenv()

api_key = os.getenv("OPENAI_API_KEY")

if not api_key:
    print("❌ Không tìm thấy OPENAI_API_KEY trong file .env")
    exit()

client = OpenAI(api_key=api_key)

try:
    response = client.chat.completions.create(
        model="gpt-4o-mini",
        messages=[
            {
                "role": "user",
                "content": "Hello, hãy trả lời đúng một từ: OK"
            }
        ],
        max_tokens=10
    )

    print("✅ Kết nối thành công!")
    print("GPT trả lời:", response.choices[0].message.content)

except Exception as e:
    print("❌ Lỗi:")
    print(e)