from functions.PY_074 import extend_blocks
import pytest
from pandas import DataFrame
from pandas.core.internals import BlockManager

class Stub:
    def __init__(self):
        self.blocks = []

def test_extend_blocks_with_list_of_lists():
    result = [[1, 2], [3, 4]]
    expected = [1, 2, 3, 4]
    assert extend_blocks(result) == expected

def test_extend_blocks_with_flat_list():
    result = [1, 2, 3, 4]
    expected = [1, 2, 3, 4]
    assert extend_blocks(result) == expected

def test_extend_blocks_with_block_manager():
    block_manager = BlockManager.from_blocks([DataFrame({'A': [1, 2]})._to_blocks()])
    expected = block_manager.blocks
    assert extend_blocks(block_manager) == expected

def test_extend_blocks_with_single_value():
    result = 42
    expected = [42]
    assert extend_blocks(result) == expected

def test_extend_blocks_with_none():
    result = None
    expected = [None]
    assert extend_blocks(result) == expected

def test_extend_blocks_with_empty_list():
    result = []
    expected = []
    assert extend_blocks(result) == expected

def test_extend_blocks_with_mixed_types():
    result = [1, [2, 3], 4]
    expected = [1, 2, 3, 4]
    assert extend_blocks(result) == expected

def test_extend_blocks_with_none_blocks():
    result = [1, 2, 3]
    expected = [1, 2, 3]
    assert extend_blocks(result, None) == expected

def test_extend_blocks_with_existing_blocks():
    result = [1, 2]
    existing_blocks = [3, 4]
    expected = [3, 4, 1, 2]
    assert extend_blocks(result, existing_blocks) == expected

def test_extend_blocks_with_block_manager_and_existing_blocks():
    block_manager = BlockManager.from_blocks([DataFrame({'A': [1, 2]})._to_blocks()])
    existing_blocks = [3, 4]
    expected = existing_blocks + block_manager.blocks
    assert extend_blocks(block_manager, existing_blocks) == expected