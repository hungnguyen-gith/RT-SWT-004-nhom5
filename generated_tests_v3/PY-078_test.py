from functions.PY_078 import is_uniform_join_units

class StubBlock:
    def __init__(self, ndim, is_extension=False):
        self.ndim = ndim
        self.is_extension = is_extension

class StubJoinUnit:
    def __init__(self, block, is_na=False, indexers=None):
        self.block = block
        self.is_na = is_na
        self.indexers = indexers if indexers is not None else []

def test_is_uniform_join_units_normal_cases():
    block1 = StubBlock(ndim=1)
    block2 = StubBlock(ndim=1)
    join_units = [StubJoinUnit(block1), StubJoinUnit(block2)]
    assert is_uniform_join_units(join_units) is True

    block3 = StubBlock(ndim=2)
    join_units = [StubJoinUnit(block3), StubJoinUnit(block3)]
    assert is_uniform_join_units(join_units) is True

def test_is_uniform_join_units_edge_cases():
    block1 = StubBlock(ndim=1)
    block2 = StubBlock(ndim=1)
    block3 = StubBlock(ndim=1)  # Different type
    join_units = [StubJoinUnit(block1), StubJoinUnit(block2), StubJoinUnit(block3)]
    assert is_uniform_join_units(join_units) is False

    block4 = StubBlock(ndim=1)
    join_units = [StubJoinUnit(block4, is_na=True), StubJoinUnit(block4)]
    assert is_uniform_join_units(join_units) is False

    join_units = [StubJoinUnit(block4, indexers=[1]), StubJoinUnit(block4)]
    assert is_uniform_join_units(join_units) is False

    block5 = StubBlock(ndim=3)
    join_units = [StubJoinUnit(block5), StubJoinUnit(block5)]
    assert is_uniform_join_units(join_units) is False

def test_is_uniform_join_units_invalid_input():
    join_units = []
    assert is_uniform_join_units(join_units) is False

    block6 = StubBlock(ndim=1)
    join_units = [StubJoinUnit(block6)]
    assert is_uniform_join_units(join_units) is False

    block7 = StubBlock(ndim=1)
    block8 = StubBlock(ndim=2)
    join_units = [StubJoinUnit(block7), StubJoinUnit(block8)]
    assert is_uniform_join_units(join_units) is False

    block9 = StubBlock(ndim=1, is_extension=True)
    join_units = [StubJoinUnit(block9, is_na=True), StubJoinUnit(block9)]
    assert is_uniform_join_units(join_units) is True