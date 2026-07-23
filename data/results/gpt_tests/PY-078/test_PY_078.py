import pytest

class MockBlock:
    def __init__(self, block_type, is_extension=False, ndim=1):
        self.block_type = block_type
        self.is_extension = is_extension
        self.ndim = ndim

class MockJoinUnit:
    def __init__(self, block, is_na=False, indexers=None):
        self.block = block
        self.is_na = is_na
        self.indexers = indexers or []

def is_uniform_join_units(join_units):
    return (
        all(type(ju.block) is type(join_units[0].block) for ju in join_units) and
        all(not ju.is_na or ju.block.is_extension for ju in join_units) and
        all(not ju.indexers for ju in join_units) and
        all(ju.block.ndim <= 2 for ju in join_units) and
        len(join_units) > 1
    )

def test_is_uniform_join_units_normal_cases():
    block1 = MockBlock(block_type='type1', is_extension=False, ndim=1)
    block2 = MockBlock(block_type='type1', is_extension=False, ndim=1)
    ju1 = MockJoinUnit(block1)
    ju2 = MockJoinUnit(block2)
    assert is_uniform_join_units([ju1, ju2]) is True

def test_is_uniform_join_units_different_types():
    block1 = MockBlock(block_type='type1', is_extension=False, ndim=1)
    block2 = MockBlock(block_type='type2', is_extension=False, ndim=1)
    ju1 = MockJoinUnit(block1)
    ju2 = MockJoinUnit(block2)
    assert is_uniform_join_units([ju1, ju2]) is False

def test_is_uniform_join_units_with_na():
    block1 = MockBlock(block_type='type1', is_extension=False, ndim=1)
    block2 = MockBlock(block_type='type1', is_extension=True, ndim=1)
    ju1 = MockJoinUnit(block1, is_na=True)
    ju2 = MockJoinUnit(block2)
    assert is_uniform_join_units([ju1, ju2]) is True

def test_is_uniform_join_units_with_indexers():
    block1 = MockBlock(block_type='type1', is_extension=False, ndim=1)
    ju1 = MockJoinUnit(block1, indexers=[1])
    ju2 = MockJoinUnit(block1)
    assert is_uniform_join_units([ju1, ju2]) is False

def test_is_uniform_join_units_high_dimensional_block():
    block1 = MockBlock(block_type='type1', is_extension=False, ndim=3)
    ju1 = MockJoinUnit(block1)
    ju2 = MockJoinUnit(block1)
    assert is_uniform_join_units([ju1, ju2]) is False

def test_is_uniform_join_units_boundary_case_empty():
    assert is_uniform_join_units([]) is False

def test_is_uniform_join_units_boundary_case_single_element():
    block1 = MockBlock(block_type='type1', is_extension=False, ndim=1)
    ju1 = MockJoinUnit(block1)
    assert is_uniform_join_units([ju1]) is False

def test_is_uniform_join_units_edge_case_extension_type():
    block1 = MockBlock(block_type='type1', is_extension=True, ndim=1)
    block2 = MockBlock(block_type='type1', is_extension=True, ndim=1)
    ju1 = MockJoinUnit(block1)
    ju2 = MockJoinUnit(block2)
    assert is_uniform_join_units([ju1, ju2]) is True