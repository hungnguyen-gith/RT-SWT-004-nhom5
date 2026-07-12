from functions.PY_082 import process_nested_expression
import pytest

class Stub:
    def _map_name(self, name):
        return name.upper()  # Simple mapping for testing

def test_process_nested_expression_single_list():
    stub = Stub()
    result = process_nested_expression(stub, [['a']])
    assert result == '(A)'

def test_process_nested_expression_multiple_leaves():
    stub = Stub()
    result = process_nested_expression(stub, ['a', 'b', 'c'])
    assert result == '(A B C)'

def test_process_nested_expression_nested():
    stub = Stub()
    result = process_nested_expression(stub, ['a', ['b', 'c']])
    assert result == '(A (B C))'

def test_process_nested_expression_lambda():
    stub = Stub()
    result = process_nested_expression(stub, ['\\', 'x', 'y', 'z'])
    assert result == '(\\ x (Y) (Z))'

def test_process_nested_expression_complex_nested():
    stub = Stub()
    result = process_nested_expression(stub, [['\\', 'x'], ['y', 'z']])
    assert result == '(\\ x (Y) (Z))'

def test_process_nested_expression_empty_list():
    stub = Stub()
    result = process_nested_expression(stub, [])
    assert result == '()'  # Assuming empty input returns empty parentheses

def test_process_nested_expression_invalid_input():
    stub = Stub()
    with pytest.raises(TypeError):
        process_nested_expression(stub, None)
    with pytest.raises(TypeError):
        process_nested_expression(stub, 123)
    with pytest.raises(TypeError):
        process_nested_expression(stub, 'string')