from functions.PY_066 import getitem_block
import pytest

class Stub:
    def __init__(self, mgr_locs, ndim, validate_ndim=True):
        self.mgr_locs = mgr_locs
        self.ndim = ndim
        self._validate_ndim = validate_ndim

    def _slice(self, slicer):
        if isinstance(slicer, int):
            return self.mgr_locs[slicer]
        elif isinstance(slicer, slice):
            return self.mgr_locs[slicer]
        elif isinstance(slicer, tuple):
            return [self.mgr_locs[s] for s in slicer]
        else:
            raise ValueError("Invalid slicer type")

    def make_block_same_class(self, new_values, new_mgr_locs):
        return new_values, new_mgr_locs

def test_getitem_block_single_index():
    stub = Stub(mgr_locs=[1, 2, 3, 4, 5], ndim=1)
    result = getitem_block(stub, 2)
    assert result == (3, 3)

def test_getitem_block_slice():
    stub = Stub(mgr_locs=[1, 2, 3, 4, 5], ndim=1)
    result = getitem_block(stub, slice(1, 4))
    assert result == ([2, 3, 4], [1, 2, 3])

def test_getitem_block_tuple():
    stub = Stub(mgr_locs=[[1, 2], [3, 4], [5, 6]], ndim=2)
    result = getitem_block(stub, (slice(0, 2), 1))
    assert result == ([3, 4], [3, 4])

def test_getitem_block_invalid_ndim():
    stub = Stub(mgr_locs=[[1, 2], [3, 4]], ndim=2)
    with pytest.raises(ValueError, match="Only same dim slicing is allowed"):
        getitem_block(stub, slice(0, 1))

def test_getitem_block_none_new_mgr_locs():
    stub = Stub(mgr_locs=[1, 2, 3, 4, 5], ndim=1)
    result = getitem_block(stub, 0, new_mgr_locs=None)
    assert result == (1, 1)

def test_getitem_block_empty_slice():
    stub = Stub(mgr_locs=[1, 2, 3, 4, 5], ndim=1)
    result = getitem_block(stub, slice(5, 5))
    assert result == ([], [])

def test_getitem_block_full_slice():
    stub = Stub(mgr_locs=[1, 2, 3, 4, 5], ndim=1)
    result = getitem_block(stub, slice(None))
    assert result == ([1, 2, 3, 4, 5], [1, 2, 3, 4, 5])