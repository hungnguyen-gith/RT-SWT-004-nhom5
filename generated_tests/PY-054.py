import pytest

def test_build_query_string_no_params():
    assert build_query_string({}) == ""

def test_build_query_string_single_param():
    assert build_query_string({"key": "value"}) == "key=value"

def test_build_query_string_multiple_params():
    assert build_query_string({"b": "2", "a": "1"}) == "a=1&b=2"

def test_build_query_string_sort_keys():
    assert build_query_string({"b": "2", "a": "1"}, sort_keys=True) == "a=1&b=2"
    assert build_query_string({"b": "2", "a": "1"}, sort_keys=False) == "b=2&a=1"

def test_build_query_string_exclude_none():
    assert build_query_string({"key": None}) == ""
    assert build_query_string({"key": None}, exclude_none=False) == "key="

def test_build_query_string_bool_values():
    assert build_query_string({"key_true": True, "key_false": False}) == "key_false=false&key_true=true"

def test_build_query_string_list_values():
    assert build_query_string({"key": [1, 2, 3]}) == "key=1&key=2&key=3"
    assert build_query_string({"key": ["a b", "c d"]}) == "key=a+b&key=c+d"

def test_build_query_string_tuple_values():
    assert build_query_string({"key": (1, 2)}) == "key=1&key=2"

def test_build_query_string_encode_spaces():
    assert build_query_string({"key": "a b c"}) == "key=a+b+c"
    assert build_query_string({"key": "a b c"}, encode_spaces=False) == "key=a b c"

def test_build_query_string_mixed_types():
    assert build_query_string({"key1": "value1", "key2": None, "key3": True, "key4": [1, 2]}) == "key1=value1&key3=true&key4=1&key4=2"