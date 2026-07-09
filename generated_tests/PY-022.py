import pytest
import numpy as np

class MockCai:
    def scaffold_analysis(self, cluster):
        return (len(cluster), len(cluster) * 2)

def jt_isim(fpsc, n):
    return np.sum(fpsc) / n if n > 0 else 0

def test_get_plot_metrics():
    cai = MockCai()
    
    # Test case 1: Normal case with multiple clusters
    clusters = [[0, 1], [2, 3, 4], [5]]
    fps = [np.array([1, 0, 0]), np.array([0, 1, 0]), np.array([0, 0, 1]), np.array([1, 1, 0]), np.array([0, 1, 1]), np.array([1, 0, 1])]
    expected_n_mol_bcs = [3, 2, 1]
    expected_n_scaff = [2, 3, 1]
    expected_isim_scaff = [2, 3, 1]
    expected_isim_clusters = [1.0, 1.0, 1.0]
    
    result = get_plot_metrics(clusters, cai, fps)
    assert result == (expected_n_mol_bcs, expected_n_scaff, expected_isim_scaff, expected_isim_clusters)

    # Test case 2: Single cluster
    clusters = [[0]]
    fps = [np.array([1, 0, 0])]
    expected_n_mol_bcs = [1]
    expected_n_scaff = [1]
    expected_isim_scaff = [1]
    expected_isim_clusters = [1.0]
    
    result = get_plot_metrics(clusters, cai, fps)
    assert result == (expected_n_mol_bcs, expected_n_scaff, expected_isim_scaff, expected_isim_clusters)

    # Test case 3: Empty clusters
    clusters = []
    fps = []
    expected_n_mol_bcs = []
    expected_n_scaff = []
    expected_isim_scaff = []
    expected_isim_clusters = []
    
    result = get_plot_metrics(clusters, cai, fps)
    assert result == (expected_n_mol_bcs, expected_n_scaff, expected_isim_scaff, expected_isim_clusters)

    # Test case 4: Clusters with varying sizes
    clusters = [[0, 1, 2], [3], [4, 5, 6, 7]]
    fps = [np.array([1, 0]), np.array([0, 1]), np.array([1, 1]), np.array([0, 0]), np.array([1, 0]), np.array([0, 1]), np.array([1, 1]), np.array([0, 0])]
    expected_n_mol_bcs = [4, 3, 1]
    expected_n_scaff = [4, 1, 2]
    expected_isim_scaff = [4, 1, 2]
    expected_isim_clusters = [1.0, 1.0, 1.0]
    
    result = get_plot_metrics(clusters, cai, fps)
    assert result == (expected_n_mol_bcs, expected_n_scaff, expected_isim_scaff, expected_isim_clusters)

    # Test case 5: Top parameter less than number of clusters
    clusters = [[0, 1], [2, 3], [4, 5]]
    fps = [np.array([1, 0]), np.array([0, 1]), np.array([1, 1]), np.array([0, 0]), np.array([1, 0]), np.array([0, 1])]
    expected_n_mol_bcs = [2, 2]
    expected_n_scaff = [2, 2]
    expected_isim_scaff = [2, 2]
    expected_isim_clusters = [1.0, 1.0]
    
    result = get_plot_metrics(clusters, cai, fps, top=2)
    assert result == (expected_n_mol_bcs, expected_n_scaff, expected_isim_scaff, expected_isim_clusters)