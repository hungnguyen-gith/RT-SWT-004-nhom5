import pytest
from unittest.mock import MagicMock
import plotly.graph_objects as go

def test_mol_relocation_plots_no_clusters():
    brc_1 = MagicMock()
    brc_2 = MagicMock()
    brc_1.get_cluster_mol_ids.return_value = []
    brc_2.get_cluster_mol_ids.return_value = []
    
    mol_relocation_plots(brc_1, brc_2, top_n=2, title="Test No Clusters")
    
    brc_1.get_cluster_mol_ids.assert_called_once()
    brc_2.get_cluster_mol_ids.assert_called_once()

def test_mol_relocation_plots_one_cluster():
    brc_1 = MagicMock()
    brc_2 = MagicMock()
    brc_1.get_cluster_mol_ids.return_value = [['A', 'B']]
    brc_2.get_cluster_mol_ids.return_value = [['A', 'C']]
    
    mol_relocation_plots(brc_1, brc_2, top_n=2, title="Test One Cluster")
    
    brc_1.get_cluster_mol_ids.assert_called_once()
    brc_2.get_cluster_mol_ids.assert_called_once()

def test_mol_relocation_plots_multiple_clusters():
    brc_1 = MagicMock()
    brc_2 = MagicMock()
    brc_1.get_cluster_mol_ids.return_value = [['A', 'B'], ['D', 'E']]
    brc_2.get_cluster_mol_ids.return_value = [['A', 'C'], ['F']]
    
    mol_relocation_plots(brc_1, brc_2, top_n=2, title="Test Multiple Clusters")
    
    brc_1.get_cluster_mol_ids.assert_called_once()
    brc_2.get_cluster_mol_ids.assert_called_once()

def test_mol_relocation_plots_top_n():
    brc_1 = MagicMock()
    brc_2 = MagicMock()
    brc_1.get_cluster_mol_ids.return_value = [['A', 'B'], ['C', 'D', 'E']]
    brc_2.get_cluster_mol_ids.return_value = [['A', 'C'], ['F']]
    
    mol_relocation_plots(brc_1, brc_2, top_n=1, title="Test Top N")
    
    brc_1.get_cluster_mol_ids.assert_called_once()
    brc_2.get_cluster_mol_ids.assert_called_once()

def test_mol_relocation_plots_empty_title():
    brc_1 = MagicMock()
    brc_2 = MagicMock()
    brc_1.get_cluster_mol_ids.return_value = [['A', 'B']]
    brc_2.get_cluster_mol_ids.return_value = [['A', 'C']]
    
    mol_relocation_plots(brc_1, brc_2, top_n=2, title="")
    
    brc_1.get_cluster_mol_ids.assert_called_once()
    brc_2.get_cluster_mol_ids.assert_called_once()