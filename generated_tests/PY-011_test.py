import pytest
import numpy as np

class MockCluster:
    def __init__(self, cluster_mol_ids):
        self.cluster_mol_ids = cluster_mol_ids

    def get_cluster_mol_ids(self):
        return self.cluster_mol_ids

    def _calc_centroid(self, X, cluster):
        return np.mean(X[cluster], axis=0)

def test_get_top_cluster_params_normal():
    cluster_mol_ids = [[0, 1], [2, 3, 4], [5]]
    mock = MockCluster(cluster_mol_ids)
    X = np.array([[1, 2], [2, 3], [3, 4], [4, 5], [5, 6], [6, 7]])
    top = 2

    top_clusters, centroids, mol_indices, data_top_clusters = mock.get_top_cluster_params(X, top)

    assert top_clusters == [[2, 3, 4], [0, 1]]
    assert np.array_equal(centroids, np.array([[3, 4], [1.5, 2.5]]))
    assert mol_indices == [2, 3, 4, 0, 1]
    assert data_top_clusters.shape == (5, 2)

def test_get_top_cluster_params_boundary():
    cluster_mol_ids = [[0], [1], [2]]
    mock = MockCluster(cluster_mol_ids)
    X = np.array([[1, 2], [2, 3], [3, 4]])
    top = 3

    top_clusters, centroids, mol_indices, data_top_clusters = mock.get_top_cluster_params(X, top)

    assert top_clusters == [[0], [1], [2]]
    assert np.array_equal(centroids, np.array([[1, 2], [2, 3], [3, 4]]))
    assert mol_indices == [0, 1, 2]
    assert data_top_clusters.shape == (3, 2)

def test_get_top_cluster_params_edge_case_empty():
    cluster_mol_ids = []
    mock = MockCluster(cluster_mol_ids)
    X = np.array([])
    top = 0

    top_clusters, centroids, mol_indices, data_top_clusters = mock.get_top_cluster_params(X, top)

    assert top_clusters == []
    assert centroids.shape == (0, 0)
    assert mol_indices == []
    assert data_top_clusters.shape == (0, 0)

def test_get_top_cluster_params_edge_case_single_cluster():
    cluster_mol_ids = [[0, 1, 2]]
    mock = MockCluster(cluster_mol_ids)
    X = np.array([[1, 2], [2, 3], [3, 4]])
    top = 1

    top_clusters, centroids, mol_indices, data_top_clusters = mock.get_top_cluster_params(X, top)

    assert top_clusters == [[0, 1, 2]]
    assert np.array_equal(centroids, np.array([[2, 3]]))
    assert mol_indices == [0, 1, 2]
    assert data_top_clusters.shape == (3, 2)

def test_get_top_cluster_params_top_greater_than_clusters():
    cluster_mol_ids = [[0, 1], [2, 3]]
    mock = MockCluster(cluster_mol_ids)
    X = np.array([[1, 2], [2, 3], [3, 4], [4, 5]])
    top = 5

    top_clusters, centroids, mol_indices, data_top_clusters = mock.get_top_cluster_params(X, top)

    assert top_clusters == [[2, 3], [0, 1]]
    assert np.array_equal(centroids, np.array([[3, 4], [1.5, 2.5]]))
    assert mol_indices == [2, 3, 0, 1]
    assert data_top_clusters.shape == (4, 2)