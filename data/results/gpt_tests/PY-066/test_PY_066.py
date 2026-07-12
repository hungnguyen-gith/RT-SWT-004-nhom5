import pytest

class TestGetItemBlock:
    class MockClass:
        def __init__(self, mgr_locs, ndim):
            self.mgr_locs = mgr_locs
            self.ndim = ndim

        def _slice(self, slicer):
            return self.mgr_locs[slicer]

        def make_block_same_class(self, new_values, new_mgr_locs):
            return new_values, new_mgr_locs

    def test_getitem_block_normal_case(self):
        obj = self.MockClass(mgr_locs=[0, 1, 2, 3, 4], ndim=1)
        result = obj.getitem_block(slice(1, 3))
        assert result == ([1, 2], [1, 2])

    def test_getitem_block_tuple_slicer(self):
        obj = self.MockClass(mgr_locs=[0, 1, 2, 3, 4], ndim=1)
        result = obj.getitem_block((slice(1, 3),))
        assert result == ([1, 2], [1, 2])

    def test_getitem_block_invalid_ndim(self):
        obj = self.MockClass(mgr_locs=[0, 1, 2, 3, 4], ndim=2)
        with pytest.raises(ValueError, match="Only same dim slicing is allowed"):
            obj.getitem_block(slice(1, 3))

    def test_getitem_block_empty_slice(self):
        obj = self.MockClass(mgr_locs=[0, 1, 2, 3, 4], ndim=1)
        result = obj.getitem_block(slice(3, 3))
        assert result == ([], [])

    def test_getitem_block_full_slice(self):
        obj = self.MockClass(mgr_locs=[0, 1, 2, 3, 4], ndim=1)
        result = obj.getitem_block(slice(None))
        assert result == ([0, 1, 2, 3, 4], [0, 1, 2, 3, 4])

    def test_getitem_block_single_element(self):
        obj = self.MockClass(mgr_locs=[0, 1, 2, 3, 4], ndim=1)
        result = obj.getitem_block(2)
        assert result == ([2], [2])

    def test_getitem_block_negative_slice(self):
        obj = self.MockClass(mgr_locs=[0, 1, 2, 3, 4], ndim=1)
        result = obj.getitem_block(slice(-3, None))
        assert result == ([2, 3, 4], [2, 3, 4])

    def test_getitem_block_none_slicer(self):
        obj = self.MockClass(mgr_locs=[0, 1, 2, 3, 4], ndim=1)
        result = obj.getitem_block(None)
        assert result == ([0, 1, 2, 3, 4], [0, 1, 2, 3, 4])