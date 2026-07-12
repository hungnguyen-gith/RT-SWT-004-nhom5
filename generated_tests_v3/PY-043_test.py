from functions.PY_043 import validate_fillna_kwargs
import pytest

class Stub:
    pass

def test_validate_fillna_kwargs_value_only():
    value, method = validate_fillna_kwargs(5, None)
    assert value == 5
    assert method is None

def test_validate_fillna_kwargs_method_only():
    value, method = validate_fillna_kwargs(None, 'ffill')
    assert value is None
    assert method == 'pad'

def test_validate_fillna_kwargs_both_none():
    with pytest.raises(ValueError, match="Must specify a fill 'value' or 'method."):
        validate_fillna_kwargs(None, None)

def test_validate_fillna_kwargs_both_specified():
    with pytest.raises(ValueError, match="Cannot specify both 'value' and 'method."):
        validate_fillna_kwargs(5, 'ffill')

def test_validate_fillna_kwargs_value_as_list():
    with pytest.raises(TypeError, match='"value" parameter must be a scalar or dict, but you passed a "list"'):
        validate_fillna_kwargs([1, 2, 3], None)

def test_validate_fillna_kwargs_value_as_tuple():
    with pytest.raises(TypeError, match='"value" parameter must be a scalar or dict, but you passed a "tuple"'):
        validate_fillna_kwargs((1, 2), None)

def test_validate_fillna_kwargs_value_as_dict():
    value, method = validate_fillna_kwargs({'key': 'value'}, None)
    assert value == {'key': 'value'}
    assert method is None

def test_validate_fillna_kwargs_value_as_none_with_method():
    value, method = validate_fillna_kwargs(None, 'bfill')
    assert value is None
    assert method == 'backfill'