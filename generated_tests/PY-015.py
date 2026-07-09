import pytest

class MockCluster:
    def __init__(self, mol_indices, n_samples):
        self.mol_indices = mol_indices
        self.n_samples_ = n_samples

class MockNode:
    def __init__(self, subclusters):
        self.subclusters_ = subclusters

class MockBRC:
    def __init__(self, leaves):
        self.leaves = leaves

    def _get_leaves(self):
        return self.leaves

def test_check_cluster_structure_no_leaves():
    brc = MockBRC([])
    check_cluster_structure(brc)

def test_check_cluster_structure_single_node_no_subclusters():
    brc = MockBRC([MockNode([])])
    check_cluster_structure(brc)

def test_check_cluster_structure_single_node_single_subcluster():
    brc = MockBRC([MockNode([MockCluster([1, 2, 3], 3)])])
    check_cluster_structure(brc)

def test_check_cluster_structure_multiple_nodes():
    brc = MockBRC([
        MockNode([MockCluster([1, 2], 2)]),
        MockNode([MockCluster([3, 4], 2)])
    ])
    check_cluster_structure(brc)

def test_check_cluster_structure_inconsistent_n_samples():
    brc = MockBRC([MockNode([MockCluster([1, 2], 3)])])
    with pytest.raises(AssertionError):
        check_cluster_structure(brc)

def test_check_cluster_structure_repeated_indices():
    brc = MockBRC([MockNode([MockCluster([1, 2, 1], 3)])])
    check_cluster_structure(brc)

def test_check_cluster_structure_unique_indices():
    brc = MockBRC([MockNode([MockCluster([1, 2, 3], 3)])])
    check_cluster_structure(brc)