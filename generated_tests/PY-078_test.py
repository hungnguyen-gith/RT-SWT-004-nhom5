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

def test_is_uniform_join_units_normal_cases():
    # Normal case with uniform blocks
    ju1 = MockJoinUnit(MockBlock(int), is_na=False)
    ju2 = MockJoinUnit(MockBlock(int), is_na=False)
    assert is_uniform_join_units([ju1, ju2]) is True

    # Normal case with extension dtype
    ju3 = MockJoinUnit(MockBlock(int, is_extension=True), is_na=True)
    assert is_uniform_join_units([ju1, ju3]) is True

def test_is_uniform_join_units_boundary_cases():
    # Boundary case with two uniform blocks
    ju4 = MockJoinUnit(MockBlock(float), is_na=False)
    assert is_uniform_join_units([ju1, ju4]) is False  # Different types

    # Boundary case with one block (should return False)
    assert is_uniform_join_units([ju1]) is False

def test_is_uniform_join_units_edge_cases():
    # Edge case with missing values and non-extension dtype
    ju5 = MockJoinUnit(MockBlock(int), is_na=True)
    assert is_uniform_join_units([ju1, ju5]) is False  # Missing value not allowed

    # Edge case with indexers present
    ju6 = MockJoinUnit(MockBlock(int), is_na=False, indexers=[1])
    assert is_uniform_join_units([ju1, ju6]) is False  # Indexers present

    # Edge case with Panel (3D block)
    ju7 = MockJoinUnit(MockBlock(int, ndim=3), is_na=False)
    assert is_uniform_join_units([ju1, ju7]) is False  # Panel not allowed

    # Edge case with empty list
    assert is_uniform_join_units([]) is False  # No blocks to concatenate