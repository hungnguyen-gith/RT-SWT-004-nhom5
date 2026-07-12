import pytest

def test_validate_fillna_kwargs_value_only():
    assert validate_fillna_kwargs(5, None) == (5, None)
    assert validate_fillna_kwargs({'key': 'value'}, None) == ({'key': 'value'}, None)

def test_validate_fillna_kwargs_method_only():
    assert validate_fillna_kwargs(None, 'ffill') == (None, 'ffill')
    assert validate_fillna_kwargs(None, 'bfill') == (None, 'bfill')

def test_validate_fillna_kwargs_both_none():
    with pytest.raises(ValueError, match="Must specify a fill 'value' or 'method'."):
        validate_fillna_kwargs(None, None)

def test_validate_fillna_kwargs_both_specified():
    with pytest.raises(ValueError, match="Cannot specify both 'value' and 'method."):
        validate_fillna_kwargs(5, 'ffill')

def test_validate_fillna_kwargs_invalid_value_type():
    with pytest.raises(TypeError, match='"value" parameter must be a scalar or dict, but you passed a "list"'):
        validate_fillna_kwargs([1, 2, 3], None)

    with pytest.raises(TypeError, match='"value" parameter must be a scalar or dict, but you passed a "tuple"'):
        validate_fillna_kwargs((1, 2), None)

def test_validate_fillna_kwargs_valid_dict_value():
    assert validate_fillna_kwargs({'key': 'value'}, None) == ({'key': 'value'}, None)

def test_validate_fillna_kwargs_valid_scalar_value():
    assert validate_fillna_kwargs(10, None) == (10, None)

def test_validate_fillna_kwargs_valid_method():
    assert validate_fillna_kwargs(None, 'ffill') == (None, 'ffill')
    assert validate_fillna_kwargs(None, 'bfill') == (None, 'bfill')

def test_validate_fillna_kwargs_invalid_method():
    with pytest.raises(ValueError, match="Cannot specify both 'value' and 'method."):
        validate_fillna_kwargs(5, 'invalid_method')