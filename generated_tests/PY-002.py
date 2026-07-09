import pytest
from unittest.mock import MagicMock

def test_split_node_leaf_with_prev_and_next():
    node = MagicMock()
    node.is_leaf = True
    node.prev_leaf_ = MagicMock()
    node.next_leaf_ = MagicMock()
    node.centroids_ = [[1, 2], [3, 4]]
    node.subclusters_ = [MagicMock(), MagicMock()]
    node.n_features = 2
    node.init_centroids_ = MagicMock(dtype='float')
    
    threshold = 0.5
    branching_factor = 2
    singly = False

    new_subcluster1, new_subcluster2 = _split_node(node, threshold, branching_factor, singly)

    assert new_subcluster1.child_.prev_leaf_ == node.prev_leaf_
    assert new_subcluster1.child_.next_leaf_ is not None
    assert new_subcluster2.child_.prev_leaf_ == new_subcluster1.child_
    assert new_subcluster2.child_.next_leaf_ == node.next_leaf_

def test_split_node_leaf_without_prev():
    node = MagicMock()
    node.is_leaf = True
    node.prev_leaf_ = None
    node.next_leaf_ = MagicMock()
    node.centroids_ = [[1, 2], [3, 4]]
    node.subclusters_ = [MagicMock(), MagicMock()]
    node.n_features = 2
    node.init_centroids_ = MagicMock(dtype='float')
    
    threshold = 0.5
    branching_factor = 2
    singly = False

    new_subcluster1, new_subcluster2 = _split_node(node, threshold, branching_factor, singly)

    assert new_subcluster1.child_.prev_leaf_ is None
    assert new_subcluster1.child_.next_leaf_ == new_subcluster2.child_
    assert new_subcluster2.child_.prev_leaf_ == new_subcluster1.child_

def test_split_node_non_leaf():
    node = MagicMock()
    node.is_leaf = False
    node.centroids_ = [[1, 2], [3, 4]]
    node.subclusters_ = [MagicMock(), MagicMock()]
    node.n_features = 2
    node.init_centroids_ = MagicMock(dtype='float')
    
    threshold = 0.5
    branching_factor = 2
    singly = False

    new_subcluster1, new_subcluster2 = _split_node(node, threshold, branching_factor, singly)

    assert new_subcluster1.child_.prev_leaf_ is None
    assert new_subcluster2.child_.prev_leaf_ is None

def test_split_node_singly():
    node = MagicMock()
    node.is_leaf = True
    node.prev_leaf_ = None
    node.next_leaf_ = None
    node.centroids_ = [[1, 2], [3, 4]]
    node.subclusters_ = [MagicMock(), MagicMock()]
    node.n_features = 2
    node.init_centroids_ = MagicMock(dtype='float')
    
    threshold = 0.5
    branching_factor = 2
    singly = True

    new_subcluster1, new_subcluster2 = _split_node(node, threshold, branching_factor, singly)

    assert new_subcluster1.child_.prev_leaf_ is None
    assert new_subcluster2.child_.prev_leaf_ is None

def test_split_node_with_equal_distances():
    node = MagicMock()
    node.is_leaf = True
    node.prev_leaf_ = None
    node.next_leaf_ = None
    node.centroids_ = [[1, 2], [1, 2]]
    node.subclusters_ = [MagicMock(), MagicMock()]
    node.n_features = 2
    node.init_centroids_ = MagicMock(dtype='float')
    
    threshold = 0.5
    branching_factor = 2
    singly = False

    new_subcluster1, new_subcluster2 = _split_node(node, threshold, branching_factor, singly)

    assert new_subcluster1.child_.prev_leaf_ is None
    assert new_subcluster2.child_.prev_leaf_ is None