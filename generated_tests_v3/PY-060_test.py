from functions.PY_060 import grade_exam
import pytest

def test_grade_exam_normal_cases():
    assert grade_exam(85, 95, False, 0, False, False) == "B"
    assert grade_exam(75, 80, False, 5, False, False) == "C"
    assert grade_exam(60, 90, False, 0, False, False) == "D"
    assert grade_exam(95, 100, False, 0, False, False) == "A"
    assert grade_exam(50, 50, False, 0, False, False) == "F"

def test_grade_exam_with_late_penalty():
    assert grade_exam(85, 95, True, 0, False, False) == "B"
    assert grade_exam(85, 95, True, 0, True, False) == "B"
    assert grade_exam(85, 95, True, 5, False, False) == "B"
    assert grade_exam(85, 95, True, 5, True, False) == "B"

def test_grade_exam_with_attendance_penalty():
    assert grade_exam(85, 40, False, 0, False, False) == "D"
    assert grade_exam(85, 40, True, 0, False, False) == "D"
    assert grade_exam(85, 70, False, 0, False, False) == "B"
    assert grade_exam(85, 70, True, 0, False, False) == "B"

def test_grade_exam_with_extra_credit():
    assert grade_exam(85, 95, False, 10, False, False) == "A"
    assert grade_exam(75, 80, False, 10, False, False) == "B"
    assert grade_exam(60, 90, False, 10, False, False) == "D"

def test_grade_exam_makeup_exam():
    assert grade_exam(90, 95, False, 0, True, False) == "B"
    assert grade_exam(85, 95, False, 0, True, False) == "B"
    assert grade_exam(95, 100, False, 0, True, False) == "A"

def test_grade_exam_disability_accommodation():
    assert grade_exam(85, 95, True, 0, False, True) == "B"
    assert grade_exam(85, 40, False, 0, False, True) == "D"
    assert grade_exam(85, 40, True, 0, False, True) == "D"

def test_grade_exam_edge_cases():
    assert grade_exam(89, 90, False, 0, False, False) == "B"
    assert grade_exam(90, 90, False, 0, False, False) == "A"
    assert grade_exam(59, 90, False, 0, False, False) == "F"
    assert grade_exam(60, 90, False, 0, False, False) == "D"

def test_grade_exam_invalid_input():
    with pytest.raises(TypeError):
        grade_exam("eighty", 90, False, 0, False, False)
    with pytest.raises(TypeError):
        grade_exam(85, "ninety", False, 0, False, False)
    with pytest.raises(TypeError):
        grade_exam(85, 90, "no", 0, False, False)