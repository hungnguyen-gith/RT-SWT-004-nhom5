import numpy as np
import pytest

def test_chi_no_clusters():
    assert chi([]) == 0

def test_chi_single_cluster():
    assert chi([np.array([[1, 2], [1, 2]])]) == 0

def test_chi_two_clusters_centroid():
    clusters = [np.array([[1, 2], [1, 2]]), np.array([[3, 4], [3, 4]])]
    assert chi(clusters, rep_type='centroid') > 0

def test_chi_two_clusters_medoid():
    clusters = [np.array([[1, 2], [1, 2]]), np.array([[3, 4], [3, 4]])]
    assert chi(clusters, rep_type='medoid') > 0

def test_chi_curated_singleton():
    clusters = [np.array([[1, 2]]), np.array([[3, 4], [3, 4]])]
    assert chi(clusters, curated=True) == 0

def test_chi_with_reps_centroid():
    clusters = [np.array([[1, 2], [1, 2]]), np.array([[3, 4], [3, 4]])]
    reps = [np.array([1, 2]), np.array([3, 4])]
    assert chi(clusters, reps=reps, rep_type='centroid') > 0

def test_chi_with_reps_medoid():
    clusters = [np.array([[1, 2], [1, 2]]), np.array([[3, 4], [3, 4]])]
    reps = [np.array([1, 2]), np.array([3, 4])]
    assert chi(clusters, reps=reps, rep_type='medoid') > 0

def test_chi_min_size():
    clusters = [np.array([[1, 2]]), np.array([[3, 4], [3, 4]])]
    assert chi(clusters, min_size=2) == 0

def test_chi_zero_division():
    clusters = [np.array([[1, 2]])]
    assert chi(clusters) == 0

def test_chi_large_clusters():
    clusters = [np.array([[1, 2]] * 10), np.array([[3, 4]] * 10)]
    assert chi(clusters) > 0

def test_chi_empty_reps():
    clusters = [np.array([[1, 2], [1, 2]])]
    assert chi(clusters, reps=[], rep_type='centroid') > 0