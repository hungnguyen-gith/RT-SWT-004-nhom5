from functions.PY_016 import reindex_indexer
import pytest
import numpy as np

class Stub:
    def __init__(self, axes, blocks, ndim):
        self.axes = axes
        self.blocks = blocks
        self.ndim = ndim

    def copy(self, deep=True):
        return Stub(self.axes, self.blocks, self.ndim)

    def _consolidate_inplace(self):
        pass

    def _slice_take_blocks_ax0(self, indexer, fill_tuple):
        return [block.take_nd(indexer, fill_tuple) for block in self.blocks]

    def _can_reindex(self, indexer):
        if np.any(np.isin(indexer, -1)):
            raise ValueError("Reindexing with -1 is not allowed.")

class Block:
    def __init__(self, data, fill_value):
        self.data = data
        self.fill_value = fill_value

    def take_nd(self, indexer, fill_tuple):
        return np.array([self.data[i] if i != -1 else fill_tuple[0] for i in indexer])

@pytest.fixture
def setup_stub():
    axes = [np.array([0, 1, 2]), np.array(['a', 'b'])]
    blocks = [Block(np.array([1, 2, 3]), fill_value=0)]
    return Stub(axes, blocks, ndim=2)

def test_reindex_indexer_no_indexer(setup_stub):
    stub = setup_stub
    new_axis = np.array([0, 1, 2, 3])
    result = reindex_indexer(stub, new_axis, None, axis=0)
    assert np.array_equal(result.axes[0], new_axis)

def test_reindex_indexer_with_indexer(setup_stub):
    stub = setup_stub
    new_axis = np.array([0, 1, 2])
    indexer = np.array([0, 1, -1])
    result = reindex_indexer(stub, new_axis, indexer, axis=0, fill_value=-1)
    expected_data = np.array([1, 2, -1])
    assert np.array_equal(result.blocks[0].data, expected_data)

def test_reindex_indexer_invalid_axis(setup_stub):
    stub = setup_stub
    new_axis = np.array([0, 1, 2])
    indexer = np.array([0, 1])
    with pytest.raises(IndexError):
        reindex_indexer(stub, new_axis, indexer, axis=2)

def test_reindex_indexer_allow_dups(setup_stub):
    stub = setup_stub
    new_axis = np.array([0, 1, 2])
    indexer = np.array([0, 1, 1])
    result = reindex_indexer(stub, new_axis, indexer, axis=0, allow_dups=True)
    expected_data = np.array([1, 2, 2])
    assert np.array_equal(result.blocks[0].data, expected_data)

def test_reindex_indexer_fill_value(setup_stub):
    stub = setup_stub
    new_axis = np.array([0, 1, 2])
    indexer = np.array([0, -1, 1])
    result = reindex_indexer(stub, new_axis, indexer, axis=0, fill_value=-1)
    expected_data = np.array([1, -1, 2])
    assert np.array_equal(result.blocks[0].data, expected_data)

def test_reindex_indexer_no_copy(setup_stub):
    stub = setup_stub
    new_axis = np.array([0, 1, 2])
    result = reindex_indexer(stub, new_axis, None, axis=0, copy=False)
    assert result is stub  # Should return the same instance if copy is False

def test_reindex_indexer_with_none_indexer_and_same_axis(setup_stub):
    stub = setup_stub
    new_axis = np.array([0, 1, 2])
    result = reindex_indexer(stub, new_axis, None, axis=0, copy=False)
    assert result is stub  # Should return the same instance if axes are the same

def test_reindex_indexer_with_none_indexer_and_different_axis(setup_stub):
    stub = setup_stub
    new_axis = np.array(['a', 'b', 'c'])
    result = reindex_indexer(stub, new_axis, None, axis=1)
    assert np.array_equal(result.axes[1], new_axis)  # Check new axis is set correctly