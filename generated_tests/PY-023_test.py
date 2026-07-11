import pytest
import os
import pandas as pd
from unittest.mock import patch, MagicMock
import matplotlib.pyplot as plt

# Assuming the function init_plot is in a module named 'plotting'
from plotting import init_plot

@pytest.fixture
def mock_csv_data():
    return pd.DataFrame({
        "Cluster": ["A", "B", "C"],
        "Number of Molecules": [10, 20, 30],
        "Number of Unique Scaffolds": [5, 10, 15],
        "iSIM": [0.1, 0.5, 0.9]
    })

def test_init_plot_normal_case(mock_csv_data):
    with patch('os.path.exists', return_value=True), \
         patch('pandas.read_csv', return_value=mock_csv_data), \
         patch('matplotlib.pyplot.show') as mock_show:
        init_plot('test', 'Test Title')
        mock_show.assert_called_once()

def test_init_plot_no_csv_file(mock_csv_data):
    with patch('os.path.exists', return_value=False) as mock_exists:
        with patch('builtins.print') as mock_print:
            init_plot('test')
            mock_print.assert_called_once_with("Error: CSV file not found at data/test_cluster_metrics.csv")

def test_init_plot_empty_dataframe():
    empty_df = pd.DataFrame(columns=["Cluster", "Number of Molecules", "Number of Unique Scaffolds", "iSIM"])
    with patch('os.path.exists', return_value=True), \
         patch('pandas.read_csv', return_value=empty_df), \
         patch('matplotlib.pyplot.show') as mock_show:
        init_plot('test')
        mock_show.assert_called_once()

def test_init_plot_boundary_case():
    boundary_df = pd.DataFrame({
        "Cluster": ["A"],
        "Number of Molecules": [0],
        "Number of Unique Scaffolds": [0],
        "iSIM": [0.0]
    })
    with patch('os.path.exists', return_value=True), \
         patch('pandas.read_csv', return_value=boundary_df), \
         patch('matplotlib.pyplot.show') as mock_show:
        init_plot('test')
        mock_show.assert_called_once()

def test_init_plot_edge_case_title():
    edge_case_df = pd.DataFrame({
        "Cluster": ["A", "B"],
        "Number of Molecules": [1, 1],
        "Number of Unique Scaffolds": [1, 1],
        "iSIM": [0.0, 1.0]
    })
    with patch('os.path.exists', return_value=True), \
         patch('pandas.read_csv', return_value=edge_case_df), \
         patch('matplotlib.pyplot.show') as mock_show:
        init_plot('test', '')
        mock_show.assert_called_once()