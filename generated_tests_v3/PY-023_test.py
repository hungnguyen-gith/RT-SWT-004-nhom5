from functions.PY_023 import init_plot
import pytest
import pandas as pd
import os
import matplotlib.pyplot as plt

# Create a temporary CSV file for testing
@pytest.fixture
def create_temp_csv(tmp_path):
    data = {
        "Cluster": ["A", "B", "C"],
        "Number of Molecules": [10, 20, 30],
        "Number of Unique Scaffolds": [5, 10, 15],
        "iSIM": [0.1, 0.5, 0.9]
    }
    df = pd.DataFrame(data)
    csv_file = tmp_path / "data" / "test_cluster_metrics.csv"
    os.makedirs(os.path.dirname(csv_file), exist_ok=True)
    df.to_csv(csv_file, index=False)
    return str(csv_file)

def test_init_plot_valid(create_temp_csv, capsys):
    init_plot("test", title="Test Title")
    captured = capsys.readouterr()
    assert "Top 20 Cluster Metrics for Test Title" in plt.gca().get_title()
    assert "Error: CSV file not found at data/test_cluster_metrics.csv" not in captured.out

def test_init_plot_no_csv(capsys):
    init_plot("non_existent", title="Non-existent Title")
    captured = capsys.readouterr()
    assert "Error: CSV file not found at data/non_existent_cluster_metrics.csv" in captured.out

def test_init_plot_without_title(create_temp_csv, capsys):
    init_plot("test", title=None)
    captured = capsys.readouterr()
    assert "Top 20 Cluster Metrics for Test" in plt.gca().get_title()

def test_init_plot_empty_csv(tmp_path, capsys):
    empty_csv = tmp_path / "data" / "empty_cluster_metrics.csv"
    os.makedirs(os.path.dirname(empty_csv), exist_ok=True)
    pd.DataFrame().to_csv(empty_csv, index=False)
    init_plot("empty", title="Empty CSV Title")
    captured = capsys.readouterr()
    assert "Error: CSV file not found at data/empty_cluster_metrics.csv" not in captured.out

def test_init_plot_invalid_data(create_temp_csv, capsys):
    invalid_data = {
        "Cluster": ["A", "B", "C"],
        "Number of Molecules": ["ten", "twenty", "thirty"],  # Invalid data types
        "Number of Unique Scaffolds": [5, 10, 15],
        "iSIM": [0.1, 0.5, 0.9]
    }
    df = pd.DataFrame(invalid_data)
    invalid_csv_file = os.path.join(os.path.dirname(create_temp_csv), "invalid_cluster_metrics.csv")
    df.to_csv(invalid_csv_file, index=False)
    init_plot("invalid", title="Invalid Data Title")
    captured = capsys.readouterr()
    assert "Error: CSV file not found at data/invalid_cluster_metrics.csv" not in captured.out

def test_init_plot_with_edge_case(create_temp_csv, capsys):
    edge_case_data = {
        "Cluster": ["A", "B", "C"],
        "Number of Molecules": [0, 0, 0],  # Edge case with zero values
        "Number of Unique Scaffolds": [0, 0, 0],
        "iSIM": [0.0, 0.0, 0.0]
    }
    df = pd.DataFrame(edge_case_data)
    edge_case_csv_file = os.path.join(os.path.dirname(create_temp_csv), "edge_case_cluster_metrics.csv")
    df.to_csv(edge_case_csv_file, index=False)
    init_plot("edge_case", title="Edge Case Title")
    captured = capsys.readouterr()
    assert "Top 20 Cluster Metrics for Edge Case Title" in plt.gca().get_title()