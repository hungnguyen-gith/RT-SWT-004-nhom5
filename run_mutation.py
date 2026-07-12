import os
import subprocess
import pandas as pd
import sqlite3
import sys

def run_cosmic_ray(func_id, module_name, test_dir, session_file):
    """Chạy Cosmic-Ray và tự động chẩn đoán nếu test gốc bị lỗi"""
    if not os.path.exists(test_dir):
        return 0.0
        
    try:
        if os.path.exists(session_file):
            os.remove(session_file)
    except:
        pass
        
    safe_test_dir = test_dir.replace('\\', '/')
    safe_python = sys.executable.replace('\\', '/')
    functions_path = os.path.abspath("functions")
    
    # 1. Đảm bảo thư mục functions là một module hợp lệ
    init_py = os.path.join(functions_path, "__init__.py")
    if not os.path.exists(init_py):
        open(init_py, 'a').close()
        
    source_file = f"functions/{module_name}.py"
    if not os.path.exists(source_file):
        source_file = f"functions/{func_id}.py"
        if not os.path.exists(source_file):
            return 0.0
            
    safe_source = source_file.replace('\\', '/')
    
    # TẠO FILE CONFIG
    toml_file = f"cr_{module_name}.toml"
    toml_content = f"""[cosmic-ray]
module-path = "{safe_source}"
timeout = 10.0
test-command = "{safe_python} -m pytest {safe_test_dir}"

[cosmic-ray.distributor]
name = "local"
"""
    with open(toml_file, "w", encoding="utf-8") as f:
        f.write(toml_content)
        
    try:
        env = os.environ.copy()
        env['PYTHONPATH'] = functions_path
        
        # Gọi trực tiếp qua module gốc của Cosmic-Ray (An toàn 100% trên Windows)
        cli_module = ["-m", "cosmic_ray.cli"]
        
        # 2. CHẠY INIT
        init_cmd = [sys.executable] + cli_module + ["init", toml_file, session_file]
        init_proc = subprocess.run(init_cmd, env=env, capture_output=True, text=True)
        
        # Kiểm tra xem có tạo được mutant nào không
        outcomes = []
        if os.path.exists(session_file):
            with sqlite3.connect(session_file) as conn:
                cursor = conn.cursor()
                cursor.execute("SELECT count(name) FROM sqlite_master WHERE type='table' AND name='work_item'")
                if cursor.fetchone()[0] == 1:
                    cursor.execute("SELECT test_outcome FROM work_item")
                    outcomes = [row[0] for row in cursor.fetchall()]
        
        if len(outcomes) == 0:
            print(f"    [!] 0 Mutant ở thư mục: {test_dir}")
            # Chạy thử test thủ công để xem tại sao baseline fail
            test_proc = subprocess.run([sys.executable, "-m", "pytest", test_dir], env=env, capture_output=True, text=True)
            if test_proc.returncode != 0:
                print(f"    -> LÝ DO: Test gốc chạy thất bại (Fail/Error)!")
                print(f"    -> Trích xuất Pytest: {test_proc.stdout.strip()[-250:]}")
            else:
                print(f"    -> LÝ DO KHÁC: {init_proc.stdout.strip()} | {init_proc.stderr.strip()}")
            return 0.0

        # 3. CHẠY EXEC
        exec_cmd = [sys.executable] + cli_module + ["exec", toml_file, session_file]
        subprocess.run(exec_cmd, env=env, capture_output=True, text=True)
        
        # 4. ĐỌC KẾT QUẢ TỪ DATABASE SAU KHI EXEC
        with sqlite3.connect(session_file) as conn:
            cursor = conn.cursor()
            cursor.execute("SELECT test_outcome FROM work_item")
            outcomes = [row[0] for row in cursor.fetchall()]
        
        # Dọn rác
        if os.path.exists(toml_file): os.remove(toml_file)
        if os.path.exists(session_file): os.remove(session_file)
        
        total = len(outcomes)
        if total == 0: return 0.0
        killed = outcomes.count('killed') + outcomes.count('timeout')
        return (killed / total) * 100.0
        
    except Exception as e:
        print(f"  [!] Lỗi ngoại lệ: {e}")
        return 0.0

def main():
    log_path = 'data/results/pynguin_batch_log.csv'
    if not os.path.exists(log_path):
        log_path = 'data/functions_manifest.csv'
        
    df_funcs = pd.read_csv(log_path)
    results = []
    
    print(f"Bắt đầu chạy Mutation Testing cho {len(df_funcs)} functions...")
    
    for idx, row in df_funcs.iterrows():
        func_id = str(row.get('function_id', row.get('func_id', ''))).strip()
        module_name = str(row.get('module_name', func_id.replace('-', '_'))).strip()
        
        print(f"\n[{idx+1}/{len(df_funcs)}] Đang phân tích {func_id}...")
        
        gpt_test_dir = f"data/results/gpt_tests/{func_id}"
        pynguin_test_dir = f"baseline/pynguin_tests/{func_id}"
        
        print(f"  - Đo GPT:")
        ms_gpt = run_cosmic_ray(func_id, module_name, gpt_test_dir, f"session_gpt_{func_id}.sqlite")
        print(f"  - Đo Pynguin:")
        ms_pynguin = run_cosmic_ray(func_id, module_name, pynguin_test_dir, f"session_pyn_{func_id}.sqlite")
        
        results.append({
            'func_id': func_id,
            'ms_gpt': round(ms_gpt, 2),
            'ms_pynguin': round(ms_pynguin, 2)
        })
        
    os.makedirs('data/results', exist_ok=True)
    df_results = pd.DataFrame(results)
    df_results.to_csv('data/results/mutation_scores.csv', index=False)
    print("\n✅ Hoàn thành! Đã lưu kết quả tại data/results/mutation_scores.csv")

if __name__ == "__main__":
    main()