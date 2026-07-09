import pytest
import numpy as np

class MockLeaf:
    def __init__(self, subclusters):
        self.subclusters_ = subclusters

class MockSubcluster:
    def __init__(self, centroid):
        self.centroid_ = centroid

class MockModel:
    def __init__(self, first_call=True, leaves=None):
        self.first_call = first_call
        self._leaves = leaves if leaves is not None else []

    def _get_leaves(self):
        return self._leaves

    def get_centroids(self):
        if self.first_call:
            raise ValueError('The model has not been fitted yet.')
        
        centroids = []
        for leaf in self._get_leaves():
            for subcluster in leaf.subclusters_:
                centroids.append(subcluster.centroid_)

        return centroids

def test_get_centroids_raises_value_error_on_first_call():
    model = MockModel(first_call=True)
    with pytest.raises(ValueError, match='The model has not been fitted yet.'):
        model.get_centroids()

def test_get_centroids_returns_empty_list_when_no_leaves():
    model = MockModel(first_call=False, leaves=[])
    assert model.get_centroids() == []

def test_get_centroids_returns_correct_centroids():
    subcluster1 = MockSubcluster(np.array([1, 2]))
    subcluster2 = MockSubcluster(np.array([3, 4]))
    leaf1 = MockLeaf([subcluster1])
    leaf2 = MockLeaf([subcluster2])
    model = MockModel(first_call=False, leaves=[leaf1, leaf2])
    
    expected_centroids = [np.array([1, 2]), np.array([3, 4])]
    assert np.array_equal(model.get_centroids(), expected_centroids)

def test_get_centroids_with_multiple_subclusters():
    subcluster1 = MockSubcluster(np.array([1, 2]))
    subcluster2 = MockSubcluster(np.array([3, 4]))
    subcluster3 = MockSubcluster(np.array([5, 6]))
    leaf1 = MockLeaf([subcluster1, subcluster2])
    leaf2 = MockLeaf([subcluster3])
    model = MockModel(first_call=False, leaves=[leaf1, leaf2])
    
    expected_centroids = [np.array([1, 2]), np.array([3, 4]), np.array([5, 6])]
    assert np.array_equal(model.get_centroids(), expected_centroids)