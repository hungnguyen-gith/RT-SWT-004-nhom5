import pytest
import numpy as np

class TestPrepareDataBFs:
    class MockClass:
        def __init__(self, first_call, BFs):
            self.first_call = first_call
            self.BFs = BFs

        def _get_BFs(self):
            return self.BFs

    def test_first_call_raises_value_error(self):
        mock_instance = self.MockClass(first_call=True, BFs=[])
        with pytest.raises(ValueError, match='The model has not been fitted yet.'):
            mock_instance.prepare_data_BFs([], 0)

    def test_no_clusters(self):
        mock_instance = self.MockClass(first_call=False, BFs=[])
        data, bigs = mock_instance.prepare_data_BFs([], 0)
        assert data == []
        assert bigs == []

    def test_one_big_cluster(self):
        class MockBF:
            def __init__(self, n_samples_, linear_sum_, mol_indices):
                self.n_samples_ = n_samples_
                self.linear_sum_ = linear_sum_
                self.mol_indices = mol_indices

        big_cluster = MockBF(5, np.array([1, 2, 3]), [1])
        mock_instance = self.MockClass(first_call=False, BFs=[big_cluster])
        data, bigs = mock_instance.prepare_data_BFs([np.array([0, 1, 2])], 0)
        assert data == []
        assert bigs == [[1, np.array([0, 1, 2]), [1]]]

    def test_multiple_clusters(self):
        class MockBF:
            def __init__(self, n_samples_, linear_sum_, mol_indices):
                self.n_samples_ = n_samples_
                self.linear_sum_ = linear_sum_
                self.mol_indices = mol_indices

        big_cluster = MockBF(5, np.array([1, 2, 3]), [1])
        small_cluster_1 = MockBF(3, np.array([4, 5]), [2])
        small_cluster_2 = MockBF(2, np.array([6]), [3])
        mock_instance = self.MockClass(first_call=False, BFs=[big_cluster, small_cluster_1, small_cluster_2])
        data, bigs = mock_instance.prepare_data_BFs([np.array([0, 1, 2]), np.array([3, 4]), np.array([5])], 0)
        assert data == [
            [3, np.array([4, 5]).astype(np.int64), [2]],
            [2, np.array([6]).astype(np.int64), [3]]
        ]
        assert bigs == [[1, np.array([0, 1, 2]), [1]]]