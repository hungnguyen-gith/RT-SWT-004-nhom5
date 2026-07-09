import pytest

class TestMergeSubcluster:
    class MockCluster:
        def __init__(self, linear_sum, n_samples, mol_indices):
            self.linear_sum_ = linear_sum
            self.n_samples_ = n_samples
            self.mol_indices = mol_indices

    def setup_method(self):
        self.cluster = self.MockCluster(10, 5, [1, 2, 3])
        self.nominee_cluster = self.MockCluster(20, 10, [4, 5, 6])
        self.threshold = 5

    def test_merge_success(self, monkeypatch):
        def mock_calc_centroid(ls, n):
            return ls / n

        def mock_jt_isim(ls, n):
            return ls / n

        monkeypatch.setattr("calc_centroid", mock_calc_centroid)
        monkeypatch.setattr("jt_isim", mock_jt_isim)

        result = self.cluster.merge_subcluster(self.nominee_cluster, self.threshold)
        assert result is True
        assert self.cluster.n_samples_ == 15
        assert self.cluster.linear_sum_ == 30
        assert self.cluster.mol_indices == [1, 2, 3, 4, 5, 6]

    def test_merge_failure(self, monkeypatch):
        def mock_calc_centroid(ls, n):
            return ls / n

        def mock_jt_isim(ls, n):
            return ls / n

        monkeypatch.setattr("calc_centroid", mock_calc_centroid)
        monkeypatch.setattr("jt_isim", mock_jt_isim)

        self.threshold = 100  # Set a high threshold to ensure failure
        result = self.cluster.merge_subcluster(self.nominee_cluster, self.threshold)
        assert result is False
        assert self.cluster.n_samples_ == 5
        assert self.cluster.linear_sum_ == 10
        assert self.cluster.mol_indices == [1, 2, 3]

    def test_merge_edge_case(self, monkeypatch):
        def mock_calc_centroid(ls, n):
            return ls / n

        def mock_jt_isim(ls, n):
            return ls / n

        monkeypatch.setattr("calc_centroid", mock_calc_centroid)
        monkeypatch.setattr("jt_isim", mock_jt_isim)

        self.threshold = 2  # Set threshold to a value that should allow merging
        result = self.cluster.merge_subcluster(self.nominee_cluster, self.threshold)
        assert result is True
        assert self.cluster.n_samples_ == 15
        assert self.cluster.linear_sum_ == 30
        assert self.cluster.mol_indices == [1, 2, 3, 4, 5, 6]