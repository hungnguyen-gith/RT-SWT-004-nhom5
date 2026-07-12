from functions.PY_011 import get_top_cluster_params
import numpy as np
import pytest

class Stub:
    def get_cluster_mol_ids(self):
        return [[0, 1], [2, 3, 4], [5], [6, 7, 8, 9]]

    def _calc_centroid(self, X, cluster):
        return np.mean(X[cluster], axis=0)

def test_get_top_cluster_params_normal():
    stub = Stub()
    X = np.array([[1, 2], [2, 3], [3, 4], [4, 5], [5, 6], [6, 7], [7, 8], [8, 9], [9, 10], [10, 11]])
    top = 2
    top_clusters, centroids, mol_indices, data_top_clusters = get_top_cluster_params(stub, X, top)

    assert top_clusters == [[2, 3, 4], [0, 1]]
    assert centroids.shape == (2, 2)
    assert len(mol_indices) == 5
    assert data_top_clusters.shape == (5, 2)

def test_get_top_cluster_params_edge_case():
    stub = Stub()
    X = np.array([[1, 2], [2, 3]])
    top = 1
    top_clusters, centroids, mol_indices, data_top_clusters = get_top_cluster_params(stub, X, top)

    assert top_clusters == [[2, 3, 4]]
    assert centroids.shape == (1, 2)
    assert len(mol_indices) == 3
    assert data_top_clusters.shape == (3, 2)

def test_get_top_cluster_params_invalid_top():
    stub = Stub()
    X = np.array([[1, 2], [2, 3], [3, 4]])
    top = 0
    top_clusters, centroids, mol_indices, data_top_clusters = get_top_cluster_params(stub, X, top)

    assert top_clusters == []
    assert centroids.shape == (0, 2)
    assert len(mol_indices) == 0
    assert data_top_clusters.shape == (0, 2)

def test_get_top_cluster_params_large_top():
    stub = Stub()
    X = np.array([[1, 2], [2, 3], [3, 4], [4, 5]])
    top = 10  # larger than the number of clusters
    top_clusters, centroids, mol_indices, data_top_clusters = get_top_cluster_params(stub, X, top)

    assert top_clusters == [[2, 3, 4], [0, 1], [5], [6, 7, 8, 9]]
    assert centroids.shape[0] == 4
    assert len(mol_indices) == 10
    assert data_top_clusters.shape[0] == 10

def test_get_top_cluster_params_empty_input():
    stub = Stub()
    X = np.array([[]])
    top = 2
    top_clusters, centroids, mol_indices, data_top_clusters = get_top_cluster_params(stub, X, top)

    assert top_clusters == [[2, 3, 4], [0, 1]]
    assert centroids.shape == (2, 0)
    assert len(mol_indices) == 5
    assert data_top_clusters.shape == (5, 0)