import pytest
import numpy as np

class TestInsertBfSubcluster:
    class MockSubcluster:
        def __init__(self, centroid, child=None):
            self.centroid_ = centroid
            self.child_ = child

        def merge_subcluster(self, subcluster, threshold):
            return False  # Mock behavior

        def update(self, subcluster):
            pass  # Mock behavior

    class MockNode:
        def __init__(self, threshold, branching_factor):
            self.subclusters_ = []
            self.threshold = threshold
            self.branching_factor = branching_factor
            self.centroids_ = np.array([])
            self.init_centroids_ = np.array([])
            self.centroids_sum = np.zeros((1, branching_factor))

        def append_subcluster(self, subcluster):
            self.subclusters_.append(subcluster)

        def update_split_subclusters(self, index, new_subcluster1, new_subcluster2):
            pass  # Mock behavior

        def insert_bf_subcluster(self, subcluster):
            if not self.subclusters_:
                self.append_subcluster(subcluster)
                return False

            threshold = self.threshold
            branching_factor = self.branching_factor

            a = np.dot(self.centroids_, subcluster.centroid_)
            sim_matrix = self.centroids_sum[0][:len(self.centroids_)] / a
            closest_index = np.argmin(sim_matrix)
            closest_subcluster = self.subclusters_[closest_index]

            if closest_subcluster.child_ is not None:
                split_child = closest_subcluster.child_.insert_bf_subcluster(subcluster)

                if not split_child:
                    closest_subcluster.update(subcluster)
                    temp = self.subclusters_[closest_index].centroid_
                    self.init_centroids_[closest_index] = temp
                    self.centroids_[closest_index] = temp
                    self.centroids_sum[0, closest_index] = np.sum(temp)
                    return False
                else:
                    new_subcluster1, new_subcluster2 = self._split_node(
                        closest_subcluster.child_,
                        threshold,
                        branching_factor
                    )
                    self.update_split_subclusters(
                        closest_index, new_subcluster1, new_subcluster2
                    )

                    if len(self.subclusters_) > self.branching_factor:
                        return True
                    return False
            else:
                merged = closest_subcluster.merge_subcluster(subcluster, self.threshold)
                if merged:
                    temp = closest_subcluster.centroid_
                    self.centroids_[closest_index] = temp
                    self.init_centroids_[closest_index] = temp
                    self.centroids_sum[0, closest_index] = np.sum(temp)
                    return False
                elif len(self.subclusters_) < self.branching_factor:
                    self.append_subcluster(subcluster)
                    return False
                else:
                    self.append_subcluster(subcluster)
                    return True

        def _split_node(self, child, threshold, branching_factor):
            return self.MockSubcluster(np.array([0])), self.MockSubcluster(np.array([0]))

    def test_insert_empty_subcluster(self):
        node = self.MockNode(threshold=0.5, branching_factor=2)
        subcluster = self.MockSubcluster(np.array([1, 1]))
        assert node.insert_bf_subcluster(subcluster) is False

    def test_insert_with_space(self):
        node = self.MockNode(threshold=0.5, branching_factor=2)
        node.centroids_ = np.array([[1, 1]])
        node.init_centroids_ = np.array([[1, 1]])
        node.subclusters_ = [self.MockSubcluster(np.array([1, 1]))]
        node.centroids_sum[0, 0] = 2
        subcluster = self.MockSubcluster(np.array([2, 2]))
        assert node.insert_bf_subcluster(subcluster) is False

    def test_insert_and_merge(self):
        node = self.MockNode(threshold=0.5, branching_factor=2)
        node.centroids_ = np.array([[1, 1]])
        node.init_centroids_ = np.array([[1, 1]])
        node.subclusters_ = [self.MockSubcluster(np.array([1, 1]))]
        node.centroids_sum[0, 0] = 2
        subcluster = self.MockSubcluster(np.array([1, 1]))
        assert node.insert_bf_subcluster(subcluster) is False

    def test_insert_and_split(self):
        node = self.MockNode(threshold=0.5, branching_factor=1)
        node.centroids_ = np.array([[1, 1]])
        node.init_centroids_ = np.array([[1, 1]])
        node.subclusters_ = [self.MockSubcluster(np.array([1, 1]))]
        node.centroids_sum[0, 0] = 2
        subcluster = self.MockSubcluster(np.array([2, 2]))
        assert node.insert_bf_subcluster(subcluster) is True

    def test_insert_with_child(self):
        child_node = self.MockNode(threshold=0.5, branching_factor=2)
        node = self.MockNode(threshold=0.5, branching_factor=2)
        node.centroids_ = np.array([[1, 1]])
        node.init_centroids_ = np.array([[1, 1]])
        child_node.centroids_ = np.array([[1, 1]])
        child_node.init_centroids_ = np.array([[1, 1]])
        child_node.subclusters_ = [self.MockSubcluster(np.array([1, 1]))]
        child_node.centroids_sum[0, 0] = 2
        subcluster = self.MockSubcluster(np.array([2, 2]), child=child_node)
        node.subclusters_ = [self.MockSubcluster(np.array([1, 1]), child=child_node)]
        assert node.insert_bf_subcluster(subcluster) is True