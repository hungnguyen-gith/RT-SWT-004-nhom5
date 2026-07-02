import os
import subprocess
import pandas as pd
import sqlite3

def run_cosmic_ray(module_name, test_dir, session_file="session.sqlite"):
    """Khởi tạo và chạy cosmic-ray, sau đó tính Mutation Score"""
    if os.path.exists(session_file):
        os.remove(session_file)
        
    try:
        # 1. Khởi tạo session
        subprocess.run(
            ["cosmic-ray", "init", "cosmic_ray.toml", session_file],
            env=dict(os.environ, TEST_DIR=test_dir),
            check=True, stdout=subprocess.DEVNULL
        )
        # 2. Thực thi mutation testing
        subprocess.run(
            ["cosmic-ray", "exec", session_file],
            check=True, stdout=subprocess.DEVNULL
        )
        
        # 3. Đọc kết quả từ SQLite database
        conn = sqlite3.connect(session_file)
        cursor = conn.cursor()
        cursor.execute("SELECT test_outcome FROM work_item")
        outcomes = [row[0] for row in cursor.fetchall()]
        conn.close()
        
        # Tính Mutation Score
        total_mutants = len(outcomes)
        if total_mutants == 0:
            return 0.0
            
        killed_mutants = outcomes.count('killed') + outcomes.count('timeout')
        return (killed_mutants / total_mutants) * 100.0
        
    except Exception as e:
        print(f"Lỗi khi chạy {module_name} tại {test_dir}: {e}")
        return 0.0

def main():
    df_funcs = pd.read_csv('data/functions.csv')
    results = []
    
    for idx, row in df_funcs.iterrows():
        func_id = row['func_id']
        func_name = row['func_name']
        print(f"Đang tính toán Mutation Score cho {func_id} ({func_name})...")
        
        gpt_test_dir = f"results/gpt_tests/{func_id}"
        pynguin_test_dir = f"baseline/pynguin_tests/{func_id}"
        
        ms_gpt = run_cosmic_ray(func_name, gpt_test_dir)
        ms_pynguin = run_cosmic_ray(func_name, pynguin_test_dir)
        
        results.append({
            'func_id': func_id,
            'ms_gpt': ms_gpt,
            'ms_pynguin': ms_pynguin
        })
        
    os.makedirs('results', exist_ok=True)
    df_results = pd.DataFrame(results)
    df_results.to_csv('results/mutation_scores.csv', index=False)
    print("Hoàn thành! Đã lưu kết quả tại results/mutation_scores.csv")

if __name__ == "__main__":
    main()