import pytest

def test_construction_error_normal_cases():
    with pytest.raises(ValueError, match="Shape of passed values is (3, 2), indices imply (3, 2)"):
        construction_error(3, (2, 3), [(0, 1), (1, 2), (2, 3)])
    
    with pytest.raises(ValueError, match="Shape of passed values is (4, 3), indices imply (4, 3)"):
        construction_error(4, (3, 4), [(0, 1), (1, 2), (2, 3), (3, 4)])

def test_construction_error_boundary_cases():
    with pytest.raises(ValueError, match="Empty data passed with indices specified."):
        construction_error(0, (0, 0), [])
    
    with pytest.raises(ValueError, match="Shape of passed values is (1, 0), indices imply (0, 1)"):
        construction_error(1, (0, 1), [0])

def test_construction_error_edge_cases():
    with pytest.raises(ValueError, match="Shape of passed values is (1,), indices imply (1,)"):
        construction_error(1, (1,), [(0,)])
    
    with pytest.raises(ValueError, match="Shape of passed values is (2, 1), indices imply (1, 2)"):
        construction_error(2, (1, 2), [(0,), (1,)])

    with pytest.raises(ValueError, match="Shape of passed values is (0,), indices imply (0,)"):
        construction_error(0, (0,), [])
    
    with pytest.raises(ValueError, match="Shape of passed values is (2, 2), indices imply (2, 2)"):
        construction_error(2, (2, 2), [(0, 1), (1, 0)])