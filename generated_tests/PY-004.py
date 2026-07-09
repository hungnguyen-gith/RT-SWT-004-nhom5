import pytest
import numpy as np

class TestFitBFs:
    class MockModel:
        def __init__(self):
            self.threshold = 0.5
            self.branching_factor = 2
            self.first_call = True
            self.index_tracker = 0

        def _get_leaves(self):
            return [self.root_]

    def test_fit_BFs_valid_input(self):
        model = self.MockModel()
        X = [(10, np.array([1, 0, 1]), [0, 1, 2])]
        result = model.fit_BFs(X)
        assert result == model

    def test_fit_BFs_invalid_input_not_list(self):
        model = self.MockModel()
        with pytest.raises(ValueError, match='The input must be a list of BitFeatures'):
            model.fit_BFs("not_a_list")

    def test_fit_BFs_invalid_input_empty_list(self):
        model = self.MockModel()
        with pytest.raises(ValueError, match='The input must be a list of BitFeatures'):
            model.fit_BFs([])

    def test_fit_BFs_invalid_input_incorrect_shape(self):
        model = self.MockModel()
        X = [(10, np.array([1, 0]), [0, 1])]
        with pytest.raises(ValueError, match='The input must be a list of BitFeatures'):
            model.fit_BFs(X)

    def test_fit_BFs_first_call_creates_root_and_dummy_leaf(self):
        model = self.MockModel()
        X = [(10, np.array([1, 0, 1]), [0, 1, 2])]
        model.fit_BFs(X)
        assert model.root_ is not None

    def test_fit_BFs_multiple_samples(self):
        model = self.MockModel()
        X = [
            (10, np.array([1, 0, 1]), [0, 1, 2]),
            (20, np.array([0, 1, 1]), [3, 4, 5])
        ]
        result = model.fit_BFs(X)
        assert result == model
        assert model.index_tracker == 2

    def test_fit_BFs_centroids_calculation(self):
        model = self.MockModel()
        X = [(10, np.array([1, 0, 1]), [0, 1, 2])]
        model.fit_BFs(X)
        assert hasattr(model, 'subcluster_centers_')