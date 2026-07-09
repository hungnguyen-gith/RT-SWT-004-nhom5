import pytest
import numpy as np
from scipy import sparse

class TestFit:
    class MockBFNode:
        def __init__(self, threshold, branching_factor, is_leaf, n_features, dtype):
            self.threshold = threshold
            self.branching_factor = branching_factor
            self.is_leaf = is_leaf
            self.n_features = n_features
            self.dtype = dtype
            self.prev_leaf = None
            self.next_leaf = None
            self.subclusters = []
        
        def insert_bf_subcluster(self, subcluster):
            self.subclusters.append(subcluster)
            return len(self.subclusters) > self.branching_factor
        
        def append_subcluster(self, subcluster):
            self.subclusters.append(subcluster)

        def centroids_(self):
            return np.array([1])  # Mocked for testing

    class MockBFSubcluster:
        def __init__(self, linear_sum, mol_indices):
            self.linear_sum = linear_sum
            self.mol_indices = mol_indices

    class MockClass:
        def __init__(self, threshold, branching_factor):
            self.threshold = threshold
            self.branching_factor = branching_factor
            self.first_call = True
            self.index_tracker = 0
            self.root_ = None
            self.dummy_leaf_ = None
            self.subcluster_centers_ = None
            self._n_features_out = None

        def _get_leaves(self):
            return [self.root_]

        def _fit(self, X, partial):
            threshold = self.threshold
            branching_factor = self.branching_factor

            n_samples, n_features = X.shape

            if self.first_call:
                self.root_ = self.MockBFNode(
                    threshold=threshold,
                    branching_factor=branching_factor,
                    is_leaf=True,
                    n_features=n_features,
                    dtype=X.dtype,
                )
                self.dummy_leaf_ = self.MockBFNode(
                    threshold=threshold,
                    branching_factor=branching_factor,
                    is_leaf=True,
                    n_features=n_features,
                    dtype=X.dtype,
                )
                self.dummy_leaf_.next_leaf = self.root_
                self.root_.prev_leaf = self.dummy_leaf_

            if not sparse.issparse(X):
                iter_func = iter
            else:
                iter_func = lambda x: x  # Mock for sparse iteration

            for sample in iter_func(X):
                subcluster = self.MockBFSubcluster(linear_sum=sample, mol_indices=[self.index_tracker])
                split = self.root_.insert_bf_subcluster(subcluster)

                if split:
                    new_subcluster1, new_subcluster2 = self.MockBFNode(
                        threshold, branching_factor, False, n_features, X.dtype), self.MockBFNode(
                        threshold, branching_factor, False, n_features, X.dtype)
                    del self.root_
                    self.root_ = self.MockBFNode(
                        threshold=threshold,
                        branching_factor=branching_factor,
                        is_leaf=False,
                        n_features=n_features,
                        dtype=X.dtype,
                    )
                    self.root_.append_subcluster(new_subcluster1)
                    self.root_.append_subcluster(new_subcluster2)
                self.index_tracker += 1

            centroids = np.concatenate([leaf.centroids_() for leaf in self._get_leaves()])
            self.subcluster_centers_ = centroids
            self._n_features_out = self.subcluster_centers_.shape[0]
            self.first_call = False
            return self

    def test_first_call_creates_root_and_dummy_leaf(self):
        model = self.MockClass(threshold=0.5, branching_factor=2)
        X = np.array([[1, 2], [3, 4]])
        model._fit(X, partial=False)
        assert model.root_ is not None
        assert model.dummy_leaf_ is not None

    def test_non_sparse_input(self):
        model = self.MockClass(threshold=0.5, branching_factor=2)
        X = np.array([[1, 2], [3, 4]])
        model._fit(X, partial=False)
        assert model.index_tracker == 2

    def test_sparse_input(self):
        model = self.MockClass(threshold=0.5, branching_factor=2)
        X = sparse.csr_matrix([[1, 2], [3, 4]])
        model._fit(X, partial=False)
        assert model.index_tracker == 2

    def test_split_node_creates_new_root(self):
        model = self.MockClass(threshold=0.5, branching_factor=1)
        X = np.array([[1, 2], [3, 4]])
        model._fit(X, partial=False)
        assert model.root_ is not None
        assert len(model.root_.subclusters) == 2

    def test_centroids_calculation(self):
        model = self.MockClass(threshold=0.5, branching_factor=2)
        X = np.array([[1, 2], [3, 4]])
        model._fit(X, partial=False)
        assert model.subcluster_centers_.shape[0] == 1

    def test_partial_fit_updates_index_tracker(self):
        model = self.MockClass(threshold=0.5, branching_factor=2)
        X1 = np.array([[1, 2]])
        model._fit(X1, partial=True)
        assert model.index_tracker == 1
        X2 = np.array([[3, 4]])
        model._fit(X2, partial=True)
        assert model.index_tracker == 2