import pytest
import numpy as np

class TestInit:
    def test_init_with_valid_params(self):
        obj = YourClass(threshold=0.5, branching_factor=3, is_leaf=True, n_features=2, dtype=np.float32)
        assert obj.threshold == 0.5
        assert obj.branching_factor == 3
        assert obj.is_leaf is True
        assert obj.n_features == 2
        assert obj.subclusters_ == []
        assert obj.init_centroids_.shape == (4, 2)
        assert obj.prev_leaf_ is None
        assert obj.next_leaf_ is None
        assert obj.centroids_sum.shape == (1, 4)

    def test_init_with_different_dtype(self):
        obj = YourClass(threshold=0.1, branching_factor=5, is_leaf=False, n_features=3, dtype=np.int32)
        assert obj.init_centroids_.dtype == np.int32
        assert obj.centroids_sum.dtype == np.int64

    def test_init_with_zero_branching_factor(self):
        obj = YourClass(threshold=0.2, branching_factor=0, is_leaf=True, n_features=1, dtype=np.float64)
        assert obj.init_centroids_.shape == (1, 1)
        assert obj.centroids_sum.shape == (1, 1)

    def test_init_with_negative_threshold(self):
        obj = YourClass(threshold=-1.0, branching_factor=2, is_leaf=False, n_features=4, dtype=np.float32)
        assert obj.threshold == -1.0

    def test_init_with_large_n_features(self):
        obj = YourClass(threshold=0.3, branching_factor=2, is_leaf=True, n_features=100, dtype=np.float64)
        assert obj.init_centroids_.shape == (3, 100)
        assert obj.centroids_sum.shape == (1, 3)