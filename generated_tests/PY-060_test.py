import pytest

def test_grade_exam_normal_cases():
    assert grade_exam(85, 95, False, 0, False, False) == "B"
    assert grade_exam(70, 80, False, 5, False, False) == "C"
    assert grade_exam(60, 90, False, 0, False, False) == "D"
    assert grade_exam(50, 40, False, 0, False, False) == "F"
    assert grade_exam(95, 100, False, 0, False, False) == "A"

def test_grade_exam_boundary_cases():
    assert grade_exam(89, 95, False, 0, False, False) == "B"
    assert grade_exam(90, 95, False, 0, False, False) == "A"
    assert grade_exam(79, 75, False, 0, False, False) == "C"
    assert grade_exam(80, 75, False, 0, False, False) == "B"
    assert grade_exam(69, 50, False, 0, False, False) == "F"
    assert grade_exam(70, 50, False, 0, False, False) == "D"

def test_grade_exam_edge_cases():
    assert grade_exam(100, 100, False, 0, False, False) == "A"
    assert grade_exam(0, 0, False, 0, False, False) == "F"
    assert grade_exam(100, 100, True, 0, False, False) == "A"
    assert grade_exam(100, 100, False, 0, True, False) == "B"
    assert grade_exam(100, 100, False, 0, False, True) == "A"
    assert grade_exam(100, 100, True, 0, True, True) == "A"

def test_grade_exam_with_late_penalty():
    assert grade_exam(85, 95, True, 0, False, False) == "B"
    assert grade_exam(85, 95, True, 5, False, False) == "B"
    assert grade_exam(85, 95, True, 0, True, False) == "B"
    assert grade_exam(85, 95, True, 0, False, True) == "B"

def test_grade_exam_with_disability_accommodation():
    assert grade_exam(85, 95, True, 0, False, True) == "B"
    assert grade_exam(85, 40, True, 0, False, True) == "D"
    assert grade_exam(85, 40, True, 5, False, True) == "D"
    assert grade_exam(85, 40, True, 0, True, True) == "D"