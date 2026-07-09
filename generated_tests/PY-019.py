import numpy as np
import pytest

# Mock functions for dependencies
def remove_singles(clusters, min_size):
    return [clust for clust in clusters if len(clust) >= min_size]

def jt_isim(linear_sum, n_samples):
    return np.sum(linear_sum) / n_samples if n_samples > 0 else 0

def calculate_centroid(linear_sum, n_samples):
    return linear_sum / n_samples if n_samples > 0 else np.zeros_like(linear_sum)

def calculate_medoid(clust):
    return np.random.randint(0, len(clust))

# The function to be tested
def clust_dispersion(clusters, reps=False, rep_type="centroid", curated=False, min_size=1):
    if not curated:
        clusters = remove_singles(clusters, min_size)
    
    n_clusters = len(clusters)
    
    if n_clusters == 1:
        return -1
    
    isim_clusts = 0
    
    if not reps:
        representatives = []
    else:
        representatives = reps
    
    for clust in clusters:
        n_samples = len(clust)
        linear_sum = np.sum(clust, axis=0)
        isim_clusts += jt_isim(linear_sum, n_samples)
        if not reps:
            if rep_type == 'centroid':
                representatives.append(calculate_centroid(linear_sum, n_samples))
            elif rep_type == 'medoid':
                medoid = calculate_medoid(clust)
                representatives.append(clust[medoid])
    
    av_isim_clusts = isim_clusts / n_clusters
    
    representatives = np.array(representatives)
    rep_linear_sum = np.sum(representatives, axis=0)
    rep_isim = jt_isim(rep_linear_sum, n_clusters)

    try:
        value = rep_isim / av_isim_clusts
    except:
        value = 0
    
    return value

# Unit tests
def test_clust_dispersion_single_cluster():
    clusters = [np.array([[1, 2], [3, 4]])]
    assert clust_dispersion(clusters) == -1

def test_clust_dispersion_no_reps():
    clusters = [np.array([[1, 2], [3, 4]]), np.array([[5, 6], [7, 8]])]
    result = clust_dispersion(clusters, reps=False, rep_type='centroid', curated=False, min_size=1)
    assert result >= 0

def test_clust_dispersion_with_reps_centroid():
    clusters = [np.array([[1, 2], [3, 4]]), np.array([[5, 6], [7, 8]])]
    reps = [np.array([2, 3]), np.array([6, 7])]
    result = clust_dispersion(clusters, reps=reps, rep_type='centroid', curated=False, min_size=1)
    assert result >= 0

def test_clust_dispersion_with_reps_medoid():
    clusters = [np.array([[1, 2], [3, 4]]), np.array([[5, 6], [7, 8]])]
    reps = []
    result = clust_dispersion(clusters, reps=reps, rep_type='medoid', curated=False, min_size=1)
    assert result >= 0

def test_clust_dispersion_curated():
    clusters = [np.array([[1, 2]]), np.array([[3, 4]])]
    result = clust_dispersion(clusters, curated=True)
    assert result >= 0

def test_clust_dispersion_min_size():
    clusters = [np.array([[1, 2]]), np.array([[3, 4]])]
    result = clust_dispersion(clusters, min_size=2)
    assert result == 0  # Since all clusters are below min_size

def test_clust_dispersion_empty_clusters():
    clusters = []
    result = clust_dispersion(clusters)
    assert result == 0  # No clusters to process

def test_clust_dispersion_zero_division():
    clusters = [np.array([[1, 2]])]
    result = clust_dispersion(clusters, reps=False)
    assert result == 0  # Should handle zero division gracefully