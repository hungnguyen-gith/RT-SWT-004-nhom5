from functions.PY_070 import construction_error
import pytest

class Stub:
    def __init__(self, block_shape):
        self.block_shape = block_shape

def test_construction_error_matching_shapes():
    construction_error(6, (2, 3), [(0, 1), (1, 2), (2, 3)])

def test_construction_error_reversed_shapes():
    construction_error(6, (3, 2), [(0, 1), (1, 2)])

def test_construction_error_empty_data():
    with pytest.raises(ValueError, match="Empty data passed with indices specified."):
        construction_error(0, (0, 3), [(0, 1), (1, 2)])

def test_construction_error_shape_mismatch():
    with pytest.raises(ValueError, match="Shape of passed values is (2, 3), indices imply (3, 2)"):
        construction_error(6, (2, 3), [(0, 1), (1, 2), (2, 3)])

def test_construction_error_shape_mismatch_with_exception():
    with pytest.raises(ValueError, match="Shape of passed values is (2, 3), indices imply (3, 2)"):
        construction_error(6, (2, 3), [(0, 1), (1, 2)], e=ValueError("Custom error message"))

def test_construction_error_invalid_tot_items():
    with pytest.raises(ValueError, match="Shape of passed values is (1, 2), indices imply (2, 3)"):
        construction_error(1, (2, 3), [(0, 1), (1, 2)])

def test_construction_error_invalid_block_shape():
    with pytest.raises(ValueError, match="Shape of passed values is (0, 2), indices imply (2, 2)"):
        construction_error(0, (2, 0), [(0, 1), (1, 2)])