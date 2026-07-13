import os
import subprocess
import pandas as pd
import json
import sys

def get_coverage_and_csr(test_target, module_name, functions_dir):
    """Đo CSR và Branch Coverage, tự động in lỗi nếu test sập"""
    
    if os.path.isdir(test_target):
        test_file = os.path.join(test_target, f"test_{module_name}.py")
        pytest_target = test_target 
    else:
        test_file = test_target
        pytest_target = test_target 

    if not os.path.exists(test_file):
        return 0, 0.0 

    # 1. Đo CSR 
    compile_proc = subprocess.run([sys.executable, '-m', 'py_compile', test_file], capture_output=True)
    csr = 1 if compile_proc.returncode == 0 else 0
    
    bc = 0.0
    if csr == 1:
        # 2. Đo Branch Coverage
        env = os.environ.copy()
        # MẸO: Thêm cả thư mục gốc và thư mục functions vào PATH để chống lỗi Import 
        env['PYTHONPATH'] = f"{os.path.abspath(functions_dir)}{os.pathsep}{os.path.abspath('.')}"
        
        if os.path.exists('.coverage'): os.remove('.coverage')
        if os.path.exists('coverage.json'): os.remove('coverage.json')
        
        # Chạy coverage (bắt lại output thay vì giấu đi)
        run_proc = subprocess.run(
            [sys.executable, '-m', 'coverage', 'run', '--branch', '--source', functions_dir, '-m', 'pytest', pytest_target],
            env=env, capture_output=True, text=True
        )
        
        subprocess.run(
            [sys.executable, '-m', 'coverage', 'json', '-o', 'coverage.json'], 
            stdout=subprocess.DEVNULL, stderr=subprocess.DEVNULL
        )
        
        if os.path.exists('coverage.json'):
            with open('coverage.json', 'r') as f:
                cov_data = json.load(f)
                for file_path, file_data in cov_data.get('files', {}).items():
                    if f"{module_name}.py" in file_path or f"{module_name}.PY" in file_path.upper():
                        summary = file_data['summary']
                        if summary['num_branches'] > 0:
                            bc = (summary['covered_branches'] / summary['num_branches']) * 100
                        else:
                            bc = summary['percent_covered'] 
                        break

        # IN LỖI ĐỂ DEBUG NẾU PYNGUIN BỊ 0.0
        if bc == 0.0 and not os.path.isdir(test_target):
            print(f"    [!] Cảnh báo: Pynguin Coverage = 0.0 cho {module_name}")
            print(f"    -> Lỗi Pytest: {run_proc.stdout.strip()[-250:]}")
            if run_proc.stderr:
                print(f"    -> Stderr: {run_proc.stderr.strip()[-250:]}")

    return csr, round(bc, 2)

def main():
    csv_path = 'data/results/pynguin_batch_log.csv'
    if not os.path.exists(csv_path):
        csv_path = 'data/functions_manifest.csv'
        
    if not os.path.exists(csv_path):
        print(f"❌ Lỗi: Không tìm thấy file {csv_path} để đọc danh sách hàm.")
        return

    df_funcs = pd.read_csv(csv_path)
    functions_dir = 'functions'
    
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
        pynguin_test_file = f"baseline/pynguin_tests/test_{module_name}.py"
        
        print(f"\n[{idx+1}/{len(df_funcs)}] Đang đo Coverage cho {func_id}...")
        
        csr_gpt, bc_gpt = get_coverage_and_csr(gpt_test_dir, module_name, functions_dir)
        _, bc_pynguin = get_coverage_and_csr(pynguin_test_file, module_name, functions_dir)
        
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