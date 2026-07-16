import os
import pandas as pd
import re

def extract_tests():
    csv_path = 'data/llm_output.csv'
    out_base_dir = 'data/results/gpt_tests'
    
    if not os.path.exists(csv_path):
        print(f"Lỗi: Không tìm thấy file {csv_path}. Hãy copy file của Huy vào thư mục data/ nhé!")
        return

    df = pd.read_csv(csv_path)
    os.makedirs(out_base_dir, exist_ok=True)
    
    # Tự động tìm cột chứa ID của hàm
    id_col = None
    for col in df.columns:
        if col.lower() in ['func_id', 'function_id', 'id', 'function']:
            id_col = col
            break
            
    # Tự động tìm cột chứa Code Test
    code_col = None
    for col in df.columns:
        if col.lower() in ['generated_test', 'source_code', 'test_code', 'code']:
            code_col = col
            break

    if not id_col:
        print(f"❌ Lỗi: Không tìm thấy cột ID nào phù hợp trong các cột: {list(df.columns)}")
        return
    if not code_col:
        print(f"❌ Lỗi: Không tìm thấy cột chứa Code Test nào phù hợp trong các cột: {list(df.columns)}")
        return

    print(f"-> Đang dùng cột định danh: '{id_col}' và cột chứa test: '{code_col}'")

    count = 0
    for idx, row in df.iterrows():
        func_id = str(row[id_col]).strip()
        raw_code = str(row[code_col])
        
        # Dọn dẹp các ký tự markdown (```python ... ```)
        code = re.sub(r'^```python\s*', '', raw_code, flags=re.MULTILINE)
        code = re.sub(r'^```\s*$', '', code, flags=re.MULTILINE)
        
        # Tạo thư mục cho từng function (VD: data/results/gpt_tests/PY-005)
        func_dir = os.path.join(out_base_dir, func_id)
        os.makedirs(func_dir, exist_ok=True)
        
        module_name = func_id.replace('-', '_')
        test_filepath = os.path.join(func_dir, f"test_{module_name}.py")
        
        with open(test_filepath, 'w', encoding='utf-8') as f:
            f.write(code.strip())
        
        count += 1
        
    print(f"✅ Đã trích xuất thành công {count} file test vào thư mục {out_base_dir}/")

if __name__ == '__main__':
    extract_tests()