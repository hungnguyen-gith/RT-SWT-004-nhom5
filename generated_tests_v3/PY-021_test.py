from functions.PY_021 import mol_relocation_plots
import pytest

class StubBrc:
    def __init__(self, clusters):
        self.clusters = clusters

    def get_cluster_mol_ids(self):
        return self.clusters

def test_mol_relocation_plots_normal_case():
    brc_1 = StubBrc([['A', 'B', 'C'], ['D', 'E']])
    brc_2 = StubBrc([['A', 'D'], ['B', 'F', 'G']])
    mol_relocation_plots(brc_1, brc_2, top_n=2, title="Test Normal Case")

def test_mol_relocation_plots_edge_case_empty_clusters():
    brc_1 = StubBrc([[], []])
    brc_2 = StubBrc([[], []])
    mol_relocation_plots(brc_1, brc_2, top_n=2, title="Test Empty Clusters")

def test_mol_relocation_plots_edge_case_single_cluster():
    brc_1 = StubBrc([['A']])
    brc_2 = StubBrc([['A']])
    mol_relocation_plots(brc_1, brc_2, top_n=1, title="Test Single Cluster")

def test_mol_relocation_plots_edge_case_different_sizes():
    brc_1 = StubBrc([['A', 'B', 'C'], ['D']])
    brc_2 = StubBrc([['A', 'D', 'E'], ['B', 'F']])
    mol_relocation_plots(brc_1, brc_2, top_n=2, title="Test Different Sizes")

def test_mol_relocation_plots_invalid_input():
    brc_1 = StubBrc([['A', 'B'], ['C']])
    brc_2 = StubBrc([['A', 'D'], ['B', 'E']])
    with pytest.raises(Exception):
        mol_relocation_plots(brc_1, brc_2, top_n='invalid', title="Test Invalid Top N")