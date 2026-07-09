import pytest
import numpy as np

class TestInsertBfSubcluster:
    class MockSubcluster:
        def __init__(self, centroid, child=None):
            self.centroid_ = centroid
            self.child_ = child
            self.parent_ = None

        def merge_subcluster(self, subcluster, threshold):
            return False  # Mock behavior

        def update(self, subcluster):
            pass  # Mock behavior

    class MockNode:
        def __init__(self, threshold, branching_factor):
            self.subclusters_ = []
            self.centroids_ = []
            self.init_centroids_ = []
            self.threshold = threshold
            self.branching_factor = branching_factor

        def append_subcluster(self, subcluster):
            self.subclusters_.append(subcluster)
            self.centroids_.append(subcluster.centroid_)
            self.init_centroids_.append(subcluster.centroid_)

        def insert_bf_subcluster(self, subcluster, set_bits, ps, singly):
            if not self.subclusters_:
                self.append_subcluster(subcluster)
                return False

            threshold = self.threshold
            branching_factor = self.branching_factor
            a = np.dot(self.centroids_, subcluster.centroid_)
            sim_matrix = a / (np.sum(self.centroids_, axis=1) + set_bits - a)
            closest_index = np.argmax(sim_matrix)
            closest_subcluster = self.subclusters_[closest_index]

            if closest_subcluster.child_ is not None:
                ps = closest_subcluster
                split_child = closest_subcluster.child_.insert_bf_subcluster(subcluster, set_bits, ps, singly)

                if not split_child:
                    closest_subcluster.update(subcluster)
                    self.init_centroids_[closest_index] = self.subclusters_[closest_index].centroid_
                    self.centroids_[closest_index] = self.subclusters_[closest_index].centroid_
                    return False
                else:
                    new_subcluster1, new_subcluster2 = self._split_node(
                        closest_subcluster.child_,
                        threshold,
                        branching_factor,
                        singly
                    )
                    self.update_split_subclusters(
                        closest_subcluster, new_subcluster1, new_subcluster2, singly
                    )

                    if len(self.subclusters_) > self.branching_factor:
                        return True
                    return False
            else:
                merged = closest_subcluster.merge_subcluster(subcluster, self.threshold)
                if merged:
                    self.centroids_[closest_index] = closest_subcluster.centroid_
                    self.init_centroids_[closest_index] = closest_subcluster.centroid_
                    if not singly:
                        closest_subcluster.parent_ = ps
                    return False
                elif len(self.subclusters_) < self.branching_factor:
                    self.append_subcluster(subcluster)
                    if not singly:
                        closest_subcluster.parent_ = ps
                    return False
                else:
                    self.append_subcluster(subcluster)
                    return True

        def _split_node(self, child, threshold, branching_factor, singly):
            return self.MockSubcluster(np.array([0])), self.MockSubcluster(np.array([0]))  # Mock behavior

        def update_split_subclusters(self, closest_subcluster, new_subcluster1, new_subcluster2, singly):
            pass  # Mock behavior

    def test_insert_empty_subclusters(self):
        node = self.MockNode(threshold=0.5, branching_factor=2)
        subcluster = self.MockSubcluster(np.array([1, 1]))
        result = node.insert_bf_subcluster(subcluster, set_bits=0, ps=None, singly=False)
        assert result is False
        assert len(node.subclusters_) == 1

    def test_insert_with_space(self):
        node = self.MockNode(threshold=0.5, branching_factor=2)
        subcluster1 = self.MockSubcluster(np.array([1, 1]))
        subcluster2 = self.MockSubcluster(np.array([2, 2]))
        node.append_subcluster(subcluster1)
        result = node.insert_bf_subcluster(subcluster2, set_bits=0, ps=None, singly=False)
        assert result is False
        assert len(node.subclusters_) == 2

    def test_insert_and_merge(self):
        node = self.MockNode(threshold=0.5, branching_factor=2)
        subcluster1 = self.MockSubcluster(np.array([1, 1]))
        subcluster2 = self.MockSubcluster(np.array([1.1, 1.1]))
        node.append_subcluster(subcluster1)
        result = node.insert_bf_subcluster(subcluster2, set_bits=0, ps=None, singly=False)
        assert result is False
        assert len(node.subclusters_) == 1

    def test_insert_and_split(self):
        node = self.MockNode(threshold=0.5, branching_factor=1)
        subcluster1 = self.MockSubcluster(np.array([1, 1]))
        subcluster2 = self.MockSubcluster(np.array([2, 2]))
        node.append_subcluster(subcluster1)
        result = node.insert_bf_subcluster(subcluster2, set_bits=0, ps=None, singly=False)
        assert result is True
        assert len(node.subclusters_) == 2

    def test_insert_with_child(self):
        node = self.MockNode(threshold=0.5, branching_factor=2)
        child = self.MockNode(threshold=0.5, branching_factor=2)
        subcluster1 = self.MockSubcluster(np.array([1, 1]), child)
        node.append_subcluster(subcluster1)
        subcluster2 = self.MockSubcluster(np.array([2, 2]))
        result = node.insert_bf_subcluster(subcluster2, set_bits=0, ps=None, singly=False)
        assert result is False
        assert len(node.subclusters_) == 1  # Assuming child handles the insertion

    def test_insert_with_full_capacity(self):
        node = self.MockNode(threshold=0.5, branching_factor=1)
        subcluster1 = self.MockSubcluster(np.array([1, 1]))
        subcluster2 = self.MockSubcluster(np.array([2, 2]))
        node.append_subcluster(subcluster1)
        node.append_subcluster(subcluster2)  # Fill to capacity
        subcluster3 = self.MockSubcluster(np.array([3, 3]))
        result = node.insert_bf_subcluster(subcluster3, set_bits=0, ps=None, singly=False)
        assert result is True  # Should trigger a split
        assert len(node.subclusters_) == 2  # Assuming split results in 2 subclusters