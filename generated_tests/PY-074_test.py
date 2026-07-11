import pytest
from pandas import BlockManager

# Assuming the function extend_blocks is imported from the module where it's defined

def test_extend_blocks_with_none():
    assert extend_blocks(None) == []

def test_extend_blocks_with_empty_list():
    assert extend_blocks([]) == []

def test_extend_blocks_with_single_element():
    assert extend_blocks(1) == [1]

def test_extend_blocks_with_list_of_integers():
    assert extend_blocks([1, 2, 3]) == [1, 2, 3]

def test_extend_blocks_with_nested_list():
    assert extend_blocks([[1, 2], [3, 4]]) == [1, 2, 3, 4]

def test_extend_blocks_with_block_manager():
    block_manager = BlockManager([1, 2, 3])
    assert extend_blocks(block_manager) == [1, 2, 3]

def test_extend_blocks_with_mixed_types():
    assert extend_blocks([1, "string", 3.5]) == [1, "string", 3.5]

def test_extend_blocks_with_none_in_list():
    assert extend_blocks([1, None, 3]) == [1, None, 3]

def test_extend_blocks_with_large_list():
    large_list = list(range(1000))
    assert extend_blocks(large_list) == large_list

def test_extend_blocks_with_empty_block_manager():
    empty_block_manager = BlockManager([])
    assert extend_blocks(empty_block_manager) == []

def test_extend_blocks_with_multiple_types_in_block_manager():
    block_manager = BlockManager([1, "text", 3.14])
    assert extend_blocks(block_manager) == [1, "text", 3.14]