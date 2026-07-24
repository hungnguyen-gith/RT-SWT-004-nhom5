import os
import py_compile
import pandas as pd

# Tạo thư mục nếu chưa có
os.makedirs("generated_tests", exist_ok=True)

# Đọc kết quả GPT sinh ra
df = pd.read_csv("results/full_llm_output.csv")

results = []
success = 0

for _, row in df.iterrows():

    function_id = row["function_id"]
    code = row["generated_test"]

    filename = f"generated_tests/{function_id}.py"

    # Ghi code test ra file
    with open(filename, "w", encoding="utf-8") as f:
        f.write(code)

    # Kiểm tra compile
    try:
        py_compile.compile(filename, doraise=True)

        csr = 1
        success += 1

        print(f"✓ {function_id}")

    except Exception:

        csr = 0

        print(f"✗ {function_id}")

    results.append({
        "function_id": function_id,
        "CSR": csr
    })

# Xuất kết quả
pd.DataFrame(results).to_csv(
    "results/bc_csr.csv",
    index=False
)

print("\n==========================")
print(f"Compile Success : {success}/{len(df)}")
print(f"CSR = {success/len(df)*100:.2f}%")