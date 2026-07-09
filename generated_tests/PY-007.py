import pytest

class TestGetClusterMolIds:
    class MockLeaf:
        def __init__(self, subclusters):
            self.subclusters_ = subclusters

    class MockSubcluster:
        def __init__(self, mol_indices):
            self.mol_indices = mol_indices

    class MockModel:
        def __init__(self, first_call, leaves):
            self.first_call = first_call
            self._leaves = leaves

        def _get_leaves(self):
            return self._leaves

    def test_get_cluster_mol_ids_first_call(self):
        model = self.MockModel(first_call=True, leaves=[])
        with pytest.raises(ValueError, match='The model has not been fitted yet.'):
            model.get_cluster_mol_ids()

    def test_get_cluster_mol_ids_no_leaves(self):
        model = self.MockModel(first_call=False, leaves=[])
        result = model.get_cluster_mol_ids()
        assert result == []

    def test_get_cluster_mol_ids_single_leaf(self):
        subcluster1 = self.MockSubcluster(mol_indices=[1, 2])
        leaf = self.MockLeaf(subclusters=[subcluster1])
        model = self.MockModel(first_call=False, leaves=[leaf])
        result = model.get_cluster_mol_ids()
        assert result == [[1, 2]]

    def test_get_cluster_mol_ids_multiple_leaves(self):
        subcluster1 = self.MockSubcluster(mol_indices=[1, 2])
        subcluster2 = self.MockSubcluster(mol_indices=[3])
        leaf1 = self.MockLeaf(subclusters=[subcluster1])
        leaf2 = self.MockLeaf(subclusters=[subcluster2])
        model = self.MockModel(first_call=False, leaves=[leaf1, leaf2])
        result = model.get_cluster_mol_ids()
        assert result == [[1, 2], [3]]

    def test_get_cluster_mol_ids_multiple_subclusters(self):
        subcluster1 = self.MockSubcluster(mol_indices=[1])
        subcluster2 = self.MockSubcluster(mol_indices=[2, 3])
        subcluster3 = self.MockSubcluster(mol_indices=[4, 5, 6])
        leaf = self.MockLeaf(subclusters=[subcluster1, subcluster2, subcluster3])
        model = self.MockModel(first_call=False, leaves=[leaf])
        result = model.get_cluster_mol_ids()
        assert result == [[4, 5, 6], [2, 3], [1]]