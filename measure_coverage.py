import os
import subprocess
import pandas as pd
import json
import sys

def get_coverage_and_csr(test_dir, module_name, functions_dir):
    """Đo CSR và Branch Coverage cho 1 bộ test"""
    test_file = os.path.join(test_dir, f"test_{module_name}.py")
    if not os.path.exists(test_file):
        return 0, 0.0  # Nếu không có file test -> fail hoàn toàn

    # 1. Đo CSR (Kiểm tra xem code test có lỗi cú pháp/compile không)
    compile_proc = subprocess.run([sys.executable, '-m', 'py_compile', test_file], capture_output=True)
    csr = 1 if compile_proc.returncode == 0 else 0
    
    bc = 0.0
    if csr == 1:
        # 2. Đo Branch Coverage bằng thư viện coverage
        env = os.environ.copy()
        env['PYTHONPATH'] = os.path.abspath(functions_dir) # Trỏ tới source code
        
        # Xóa report cũ tránh nhầm lẫn
        if os.path.exists('.coverage'): os.remove('.coverage')
        if os.path.exists('coverage.json'): os.remove('coverage.json')
        
        # Chạy coverage run (ẩn output báo lỗi test fail)
        subprocess.run(
            [sys.executable, '-m', 'coverage', 'run', '--branch', '--source', functions_dir, '-m', 'pytest', test_dir],
            env=env, stdout=subprocess.DEVNULL, stderr=subprocess.DEVNULL
        )
        # Xuất report ra JSON để đọc
        subprocess.run(
            [sys.executable, '-m', 'coverage', 'json', '-o', 'coverage.json'], 
            stdout=subprocess.DEVNULL, stderr=subprocess.DEVNULL
        )
        
        # Đọc file JSON để lấy phần trăm Branch Coverage
        if os.path.exists('coverage.json'):
            with open('coverage.json', 'r') as f:
                cov_data = json.load(f)
                for file_path, file_data in cov_data['files'].items():
                    if f"{module_name}.py" in file_path or f"{module_name}.PY" in file_path.upper():
                        summary = file_data['summary']
                        if summary['num_branches'] > 0:
                            bc = (summary['covered_branches'] / summary['num_branches']) * 100
                        else:
                            bc = summary['percent_covered'] # Dự phòng nếu không có branch
                        break

    return csr, round(bc, 2)

def main():
    # Tự động tìm file danh sách hàm chính xác của dự án
    csv_path = 'data/results/pynguin_batch_log.csv'
    if not os.path.exists(csv_path):
        csv_path = 'data/functions_manifest.csv'
        
    if not os.path.exists(csv_path):
        print(f"❌ Lỗi: Không tìm thấy file {csv_path} để đọc danh sách hàm.")
        return

    df_funcs = pd.read_csv(csv_path)
    functions_dir = 'functions'
    
    # Tự động nhận diện cột ID
    id_col = None
    for col in df_funcs.columns:
        if col.lower() in ['func_id', 'function_id', 'id']:
            id_col = col
            break
            
    if not id_col:
        print("❌ Lỗi: Không tìm thấy cột chứa ID hàm trong file CSV.")
        return

    results = []
    print(f"Bắt đầu đo Coverage & CSR cho {len(df_funcs)} functions từ '{csv_path}'...")
    
    for idx, row in df_funcs.iterrows():
        func_id = str(row[id_col]).strip()
        module_name = func_id.replace('-', '_')
        
        gpt_test_dir = f"data/results/gpt_tests/{func_id}"
        pynguin_test_dir = f"baseline/pynguin_tests/{func_id}"
        
        print(f"[{idx+1}/{len(df_funcs)}] Đang đo Coverage cho {func_id}...")
        csr_gpt, bc_gpt = get_coverage_and_csr(gpt_test_dir, module_name, functions_dir)
        _, bc_pynguin = get_coverage_and_csr(pynguin_test_dir, module_name, functions_dir)
        
        results.append({
            'func_id': func_id,
            'bc_gpt': bc_gpt,
            'bc_pynguin': bc_pynguin,
            'csr_gpt': csr_gpt
        })
        
    os.makedirs('data/results', exist_ok=True)
    df_res = pd.DataFrame(results)
    df_res.to_csv('data/results/bc_csr.csv', index=False)
    print("\n✅ Hoàn thành! Đã lưu kết quả tại data/results/bc_csr.csv")

if __name__ == '__main__':
    main()