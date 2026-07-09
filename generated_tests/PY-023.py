import os
import pandas as pd
import matplotlib.pyplot as plt
import numpy as np
import pytest
from unittest.mock import patch, MagicMock

def test_init_plot_file_not_found():
    with patch('os.path.exists', return_value=False):
        with patch('builtins.print') as mock_print:
            init_plot('test_method')
            mock_print.assert_called_once_with("Error: CSV file not found at data/test_method_cluster_metrics.csv")

def test_init_plot_file_found():
    mock_df = pd.DataFrame({
        'Cluster': ['A', 'B', 'C'],
        'Number of Molecules': [10, 20, 30],
        'Number of Unique Scaffolds': [5, 10, 15],
        'iSIM': [0.1, 0.5, 0.9]
    })
    
    with patch('os.path.exists', return_value=True), \
         patch('pandas.read_csv', return_value=mock_df), \
         patch('matplotlib.pyplot.show') as mock_show:
        
        init_plot('test_method', title='Test Title')
        mock_show.assert_called_once()

def test_init_plot_file_found_no_title():
    mock_df = pd.DataFrame({
        'Cluster': ['A', 'B', 'C'],
        'Number of Molecules': [10, 20, 30],
        'Number of Unique Scaffolds': [5, 10, 15],
        'iSIM': [0.1, 0.5, 0.9]
    })
    
    with patch('os.path.exists', return_value=True), \
         patch('pandas.read_csv', return_value=mock_df), \
         patch('matplotlib.pyplot.show') as mock_show:
        
        init_plot('test_method')
        mock_show.assert_called_once()