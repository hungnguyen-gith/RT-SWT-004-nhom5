import os
import subprocess
import pandas as pd
import sqlite3

def run_cosmic_ray(module_name, test_dir, session_file="session.sqlite"):
    """Khởi tạo và chạy cosmic-ray, sau đó tính Mutation Score"""
    if os.path.exists(session_file):
        os.remove(session_file)
        
    try:
        subprocess.run(
            ["cosmic-ray", "init", "cosmic_ray.toml", session_file],
            env=dict(os.environ, TEST_DIR=test_dir),
            check=True, stdout=subprocess.DEVNULL, stderr=subprocess.DEVNULL
        )
        subprocess.run(
            ["cosmic-ray", "exec", session_file],
            check=True, stdout=subprocess.DEVNULL, stderr=subprocess.DEVNULL
        )
        
        conn = sqlite3.connect(session_file)
        cursor = conn.cursor()
        cursor.execute("SELECT test_outcome FROM work_item")
        outcomes = [row[0] for row in cursor.fetchall()]
        conn.close()
        
        total_mutants = len(outcomes)
        if total_mutants == 0:
            return 0.0
            
        killed_mutants = outcomes.count('killed') + outcomes.count('timeout')
        return (killed_mutants / total_mutants) * 100.0
        
    except Exception as e:
        print(f"[!] Lỗi khi chạy mutation cho {module_name} tại {test_dir}: {e}")
        return 0.0

def main():
    log_path = 'data/results/pynguin_batch_log.csv'
    if not os.path.exists(log_path):
        print(f"Không tìm thấy {log_path}. Hãy kiểm tra lại!")
        return
        
    df_funcs = pd.read_csv(log_path)
    results = []
    
    print(f"Bắt đầu chạy Mutation Testing cho {len(df_funcs)} functions...")
    
    for idx, row in df_funcs.iterrows():
        func_id = row['function_id']
        module_name = row['module_name']
        print(f"[{idx+1}/{len(df_funcs)}] Tính Mutation Score: {func_id}...")
        
        gpt_test_dir = f"data/results/gpt_tests/{func_id}"
        pynguin_test_dir = f"baseline/pynguin_tests/{func_id}"
        
        ms_gpt = run_cosmic_ray(module_name, gpt_test_dir) if os.path.exists(gpt_test_dir) else 0.0
        ms_pynguin = run_cosmic_ray(module_name, pynguin_test_dir) if os.path.exists(pynguin_test_dir) else 0.0
        
        results.append({
            'func_id': func_id,
            'ms_gpt': round(ms_gpt, 2),
            'ms_pynguin': round(ms_pynguin, 2)
        })
        
    os.makedirs('data/results', exist_ok=True)
    df_results = pd.DataFrame(results)
    df_results.to_csv('data/results/mutation_scores.csv', index=False)
    print("\nHoàn thành! Đã lưu kết quả tại data/results/mutation_scores.csv")

if __name__ == "__main__":
    main()