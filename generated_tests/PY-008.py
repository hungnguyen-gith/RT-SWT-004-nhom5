import pytest

class TestGetBFs:
    class MockLeaf:
        def __init__(self, subclusters):
            self.subclusters_ = subclusters

    class MockModel:
        def __init__(self, first_call, leaves):
            self.first_call = first_call
            self.leaves = leaves

        def _get_leaves(self):
            return self.leaves

    def test_get_BFs_raises_value_error_when_first_call(self):
        model = self.MockModel(first_call=True, leaves=[])
        with pytest.raises(ValueError, match='The model has not been fitted yet.'):
            model._get_BFs()

    def test_get_BFs_returns_empty_list_when_no_leaves(self):
        model = self.MockModel(first_call=False, leaves=[])
        result = model._get_BFs()
        assert result == []

    def test_get_BFs_returns_sorted_BFs(self):
        subcluster1 = type('Subcluster', (object,), {'n_samples_': 5})
        subcluster2 = type('Subcluster', (object,), {'n_samples_': 10})
        subcluster3 = type('Subcluster', (object,), {'n_samples_': 3})
        
        leaf1 = self.MockLeaf(subclusters=[subcluster1, subcluster2])
        leaf2 = self.MockLeaf(subclusters=[subcluster3])
        
        model = self.MockModel(first_call=False, leaves=[leaf1, leaf2])
        result = model._get_BFs()
        
        assert result == [subcluster2, subcluster1, subcluster3]

    def test_get_BFs_with_multiple_leaves(self):
        subcluster1 = type('Subcluster', (object,), {'n_samples_': 1})
        subcluster2 = type('Subcluster', (object,), {'n_samples_': 2})
        subcluster3 = type('Subcluster', (object,), {'n_samples_': 3})
        
        leaf1 = self.MockLeaf(subclusters=[subcluster1])
        leaf2 = self.MockLeaf(subclusters=[subcluster2, subcluster3])
        
        model = self.MockModel(first_call=False, leaves=[leaf1, leaf2])
        result = model._get_BFs()
        
        assert result == [subcluster3, subcluster2, subcluster1]