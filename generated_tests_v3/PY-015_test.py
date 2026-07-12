from functions.PY_015 import check_cluster_structure
import pytest

class StubCluster:
    def __init__(self, mol_indices, n_samples):
        self.mol_indices = mol_indices
        self.n_samples_ = n_samples

class StubNode:
    def __init__(self, subclusters):
        self.subclusters_ = subclusters

class StubBRC:
    def __init__(self, leaves):
        self.leaves = leaves

    def _get_leaves(self):
        return self.leaves

def test_check_cluster_structure_valid():
    subcluster1 = StubCluster([1, 2, 3], 3)
    subcluster2 = StubCluster([4, 5], 2)
    node1 = StubNode([subcluster1])
    node2 = StubNode([subcluster2])
    brc = StubBRC([node1, node2])
    
    check_cluster_structure(brc)

def test_check_cluster_structure_repeated_indices(capsys):
    subcluster1 = StubCluster([1, 2, 3], 3)
    subcluster2 = StubCluster([2, 4], 2)  # Repeated index '2'
    node1 = StubNode([subcluster1])
    node2 = StubNode([subcluster2])
    brc = StubBRC([node1, node2])
    
    check_cluster_structure(brc)
    
    captured = capsys.readouterr()
    assert "Fatal! Index 2 is repeating!" in captured.out

def test_check_cluster_structure_empty_subclusters(capsys):
    subcluster1 = StubCluster([], 0)
    node1 = StubNode([subcluster1])
    brc = StubBRC([node1])
    
    check_cluster_structure(brc)
    
    captured = capsys.readouterr()
    assert "There are no repeated indices." in captured.out

def test_check_cluster_structure_single_node(capsys):
    subcluster1 = StubCluster([1], 1)
    node1 = StubNode([subcluster1])
    brc = StubBRC([node1])
    
    check_cluster_structure(brc)
    
    captured = capsys.readouterr()
    assert "Total number of molecules: 1" in captured.out
    assert "The range of molecular indices is 1 thru 1" in captured.out

def test_check_cluster_structure_multiple_nodes(capsys):
    subcluster1 = StubCluster([1, 2], 2)
    subcluster2 = StubCluster([3, 4], 2)
    node1 = StubNode([subcluster1])
    node2 = StubNode([subcluster2])
    brc = StubBRC([node1, node2])
    
    check_cluster_structure(brc)
    
    captured = capsys.readouterr()
    assert "Total number of molecules: 4" in captured.out
    assert "The range of molecular indices is 1 thru 4" in captured.out

def test_check_cluster_structure_inconsistent_n_samples():
    subcluster1 = StubCluster([1, 2], 3)  # Inconsistent n_samples
    node1 = StubNode([subcluster1])
    brc = StubBRC([node1])
    
    with pytest.raises(AssertionError):
        check_cluster_structure(brc)