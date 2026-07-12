import pytest

def test_grade_exam():
    # Normal test cases
    assert grade_exam(85, 95, False, 0, False, False) == "B"
    assert grade_exam(75, 80, False, 5, False, False) == "C"
    assert grade_exam(60, 50, False, 0, False, False) == "F"
    assert grade_exam(90, 100, False, 0, False, False) == "A"
    
    # Boundary test cases
    assert grade_exam(89, 50, False, 0, False, False) == "B"
    assert grade_exam(80, 74, False, 0, False, False) == "B"
    assert grade_exam(70, 74, False, 0, False, False) == "C"
    assert grade_exam(60, 89, False, 0, False, False) == "F"
    
    # Edge cases
    assert grade_exam(100, 100, False, 0, False, False) == "A"
    assert grade_exam(100, 100, True, 0, False, False) == "A"
    assert grade_exam(100, 100, False, 0, True, False) == "B"
    assert grade_exam(100, 100, False, 0, False, True) == "A"
    assert grade_exam(0, 0, False, 0, False, False) == "F"
    assert grade_exam(0, 0, False, 0, False, True) == "F"
    assert grade_exam(0, 90, False, 0, False, False) == "D"
    assert grade_exam(0, 90, False, 0, False, True) == "D"