import numpy as np
import pytest

def test_dbi_no_reps():
    clusters = [np.array([[1, 2], [1, 3]]), np.array([[4, 5], [5, 6]])]
    result = dbi(clusters, reps=False, rep_type='centroid', curated=False, min_size=1)
    assert result >= 0

def test_dbi_with_centroid_reps():
    clusters = [np.array([[1, 2], [1, 3]]), np.array([[4, 5], [5, 6]])]
    reps = [np.array([1, 2]), np.array([5, 6])]
    result = dbi(clusters, reps=reps, rep_type='centroid', curated=False, min_size=1)
    assert result >= 0

def test_dbi_with_medoid_reps():
    clusters = [np.array([[1, 2], [1, 3]]), np.array([[4, 5], [5, 6]])]
    reps = [np.array([1, 3]), np.array([5, 6])]
    result = dbi(clusters, reps=reps, rep_type='medoid', curated=False, min_size=1)
    assert result >= 0

def test_dbi_curated_clusters():
    clusters = [np.array([[1, 2]]), np.array([[4, 5], [5, 6]])]
    result = dbi(clusters, reps=False, rep_type='centroid', curated=True, min_size=1)
    assert result >= 0

def test_dbi_empty_clusters():
    clusters = []
    result = dbi(clusters, reps=False, rep_type='centroid', curated=False, min_size=1)
    assert result == 0

def test_dbi_singleton_clusters():
    clusters = [np.array([[1, 2]])]
    result = dbi(clusters, reps=False, rep_type='centroid', curated=False, min_size=2)
    assert result == 0

def test_dbi_min_size_filter():
    clusters = [np.array([[1, 2]]), np.array([[3, 4], [4, 5]])]
    result = dbi(clusters, reps=False, rep_type='centroid', curated=False, min_size=2)
    assert result >= 0

def test_dbi_zero_division():
    clusters = [np.array([[1, 2]])]
    result = dbi(clusters, reps=False, rep_type='centroid', curated=False, min_size=1)
    assert result == 0

def test_dbi_invalid_rep_type():
    clusters = [np.array([[1, 2], [1, 3]]), np.array([[4, 5], [5, 6]])]
    with pytest.raises(ValueError):
        dbi(clusters, reps=False, rep_type='invalid', curated=False, min_size=1)