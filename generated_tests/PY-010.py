import pytest
from unittest.mock import MagicMock

class TestGetPruneIndices:
    def test_no_clusters(self):
        obj = MagicMock()
        obj._get_leaves.return_value = []
        assert obj._get_prune_indices() == lazyPrune(None, None, obj)

    def test_single_leaf_no_clusters(self):
        obj = MagicMock()
        obj._get_leaves.return_value = [MagicMock(subclusters_=[])]
        assert obj._get_prune_indices() == lazyPrune(None, None, obj)

    def test_single_leaf_single_cluster(self):
        cluster = MagicMock(mol_indices=[1, 2, 3])
        leaf = MagicMock(subclusters_=[cluster])
        obj = MagicMock()
        obj._get_leaves.return_value = [leaf]
        assert obj._get_prune_indices() == lazyPrune(0, 0, obj)

    def test_multiple_leaves_multiple_clusters(self):
        cluster1 = MagicMock(mol_indices=[1, 2])
        cluster2 = MagicMock(mol_indices=[1, 2, 3, 4])
        leaf1 = MagicMock(subclusters_=[cluster1])
        leaf2 = MagicMock(subclusters_=[cluster2])
        obj = MagicMock()
        obj._get_leaves.return_value = [leaf1, leaf2]
        assert obj._get_prune_indices() == lazyPrune(1, 0, obj)

    def test_multiple_leaves_same_size_clusters(self):
        cluster1 = MagicMock(mol_indices=[1, 2])
        cluster2 = MagicMock(mol_indices=[3, 4])
        leaf1 = MagicMock(subclusters_=[cluster1])
        leaf2 = MagicMock(subclusters_=[cluster2])
        obj = MagicMock()
        obj._get_leaves.return_value = [leaf1, leaf2]
        assert obj._get_prune_indices() == lazyPrune(0, 0, obj)  # First cluster should be chosen

    def test_empty_mol_indices(self):
        cluster = MagicMock(mol_indices=[])
        leaf = MagicMock(subclusters_=[cluster])
        obj = MagicMock()
        obj._get_leaves.return_value = [leaf]
        assert obj._get_prune_indices() == lazyPrune(0, 0, obj)  # Should handle empty mol_indices correctly