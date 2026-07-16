import pytest
import os
import pandas as pd
from unittest.mock import patch, MagicMock
import matplotlib.pyplot as plt

# Assuming the function init_plot is in a module named 'plotting'
from plotting import init_plot

@pytest.fixture
def mock_csv_data(tmp_path):
    data = {
        "Cluster": ["A", "B", "C"],
        "Number of Molecules": [10, 20, 30],
        "Number of Unique Scaffolds": [5, 10, 15],
        "iSIM": [0.1, 0.5, 0.9]
    }
    df = pd.DataFrame(data)
    csv_file = tmp_path / "data/method_cluster_metrics.csv"
    df.to_csv(csv_file, index=False)
    return csv_file

def test_init_plot_normal_case(mock_csv_data):
    with patch("os.path.exists", return_value=True), patch("pandas.read_csv", return_value=pd.read_csv(mock_csv_data)):
        init_plot("method")

def test_init_plot_with_title(mock_csv_data):
    with patch("os.path.exists", return_value=True), patch("pandas.read_csv", return_value=pd.read_csv(mock_csv_data)):
        init_plot("method", title="Test Title")

def test_init_plot_file_not_found():
    with patch("os.path.exists", return_value=False):
        with patch("builtins.print") as mock_print:
            init_plot("method")
            mock_print.assert_called_once_with("Error: CSV file not found at data/method_cluster_metrics.csv")

def test_init_plot_empty_dataframe(tmp_path):
    empty_df = pd.DataFrame(columns=["Cluster", "Number of Molecules", "Number of Unique Scaffolds", "iSIM"])
    empty_csv = tmp_path / "data/empty_cluster_metrics.csv"
    empty_df.to_csv(empty_csv, index=False)

    with patch("os.path.exists", return_value=True), patch("pandas.read_csv", return_value=pd.read_csv(empty_csv)):
        with patch("builtins.print") as mock_print:
            init_plot("method")
            mock_print.assert_called_once_with("Error: CSV file not found at data/method_cluster_metrics.csv")

def test_init_plot_boundary_case(mock_csv_data):
    data = {
        "Cluster": ["A", "B"],
        "Number of Molecules": [0, 0],
        "Number of Unique Scaffolds": [0, 0],
        "iSIM": [0.0, 1.0]
    }
    df = pd.DataFrame(data)
    csv_file = mock_csv_data.parent / "boundary_cluster_metrics.csv"
    df.to_csv(csv_file, index=False)

    with patch("os.path.exists", return_value=True), patch("pandas.read_csv", return_value=pd.read_csv(csv_file)):
        init_plot("method")

def test_init_plot_edge_case(mock_csv_data):
    data = {
        "Cluster": ["A"],
        "Number of Molecules": [1],
        "Number of Unique Scaffolds": [1],
        "iSIM": [0.5]
    }
    df = pd.DataFrame(data)
    csv_file = mock_csv_data.parent / "edge_cluster_metrics.csv"
    df.to_csv(csv_file, index=False)

    with patch("os.path.exists", return_value=True), patch("pandas.read_csv", return_value=pd.read_csv(csv_file)):
        init_plot("method")