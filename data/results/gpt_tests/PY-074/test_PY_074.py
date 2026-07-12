import pytest
from pandas import DataFrame
from pandas.core.internals import BlockManager

# Assuming the function extend_blocks is defined in a module named my_module
from my_module import extend_blocks

def test_extend_blocks_with_none():
    assert extend_blocks(None) == [None]

def test_extend_blocks_with_empty_list():
    assert extend_blocks([]) == []

def test_extend_blocks_with_single_element():
    assert extend_blocks(5) == [5]

def test_extend_blocks_with_list_of_integers():
    assert extend_blocks([1, 2, 3]) == [1, 2, 3]

def test_extend_blocks_with_nested_list():
    assert extend_blocks([[1, 2], [3, 4]]) == [1, 2, 3, 4]

def test_extend_blocks_with_block_manager():
    df = DataFrame({'A': [1, 2], 'B': [3, 4]})
    block_manager = df._mgr
    result = extend_blocks(block_manager)
    assert len(result) == len(block_manager.blocks)

def test_extend_blocks_with_mixed_types():
    assert extend_blocks([1, 'a', [2, 3]]) == [1, 'a', 2, 3]

def test_extend_blocks_with_none_in_list():
    assert extend_blocks([1, None, 3]) == [1, None, 3]

def test_extend_blocks_with_large_list():
    large_list = list(range(1000))
    assert extend_blocks(large_list) == large_list

def test_extend_blocks_with_empty_block_manager():
    empty_block_manager = BlockManager([])
    assert extend_blocks(empty_block_manager) == []

def test_extend_blocks_with_multiple_types():
    assert extend_blocks([1, [2, 'b'], 3.5]) == [1, 2, 'b', 3.5]