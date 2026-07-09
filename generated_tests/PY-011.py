import pytest
import numpy as np

class TestGetTopClusterParams:
    class MockCluster:
        def get_cluster_mol_ids(self):
            return [[0, 1], [2, 3, 4], [5]]

        def _calc_centroid(self, X, cluster):
            return np.mean(X[cluster], axis=0)

    def setup_method(self):
        self.mock = self.MockCluster()
        self.X = np.array([[1, 2], [2, 3], [3, 4], [4, 5], [5, 6], [6, 7]])
        self.top = 2

    def test_get_top_cluster_params(self):
        top_clusters, centroids, mol_indices, data_top_clusters = self.mock._get_top_cluster_params(self.X, self.top)
        assert top_clusters == [[2, 3, 4], [0, 1]]
        assert np.array_equal(centroids, np.array([[4, 5], [1.5, 2.5]]))
        assert mol_indices == [2, 3, 4, 0, 1]
        assert data_top_clusters.shape[0] == len(mol_indices)

    def test_get_top_cluster_params_with_single_cluster(self):
        self.mock.get_cluster_mol_ids = lambda: [[0]]
        top_clusters, centroids, mol_indices, data_top_clusters = self.mock._get_top_cluster_params(self.X, self.top)
        assert top_clusters == [[0]]
        assert np.array_equal(centroids, np.array([[1, 2]]))
        assert mol_indices == [0]
        assert data_top_clusters.shape[0] == len(mol_indices)

    def test_get_top_cluster_params_with_empty_clusters(self):
        self.mock.get_cluster_mol_ids = lambda: []
        top_clusters, centroids, mol_indices, data_top_clusters = self.mock._get_top_cluster_params(self.X, self.top)
        assert top_clusters == []
        assert centroids.shape == (0, self.X.shape[1])
        assert mol_indices == []
        assert data_top_clusters.shape[0] == 0

    def test_get_top_cluster_params_with_more_clusters_than_top(self):
        self.mock.get_cluster_mol_ids = lambda: [[0], [1], [2], [3], [4]]
        top_clusters, centroids, mol_indices, data_top_clusters = self.mock._get_top_cluster_params(self.X, 3)
        assert top_clusters == [[4], [3], [2]]
        assert np.array_equal(centroids, np.array([[5, 6], [4, 5], [3, 4]]))
        assert mol_indices == [4, 3, 2]
        assert data_top_clusters.shape[0] == len(mol_indices)