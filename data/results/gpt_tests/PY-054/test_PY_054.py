import pytest

def test_build_query_string_normal_cases():
    assert build_query_string({'a': 1, 'b': 2}) == 'a=1&b=2'
    assert build_query_string({'name': 'John Doe', 'age': 30}) == 'age=30&name=John+Doe'
    assert build_query_string({'key': True, 'value': False}) == 'key=true&value=false'
    assert build_query_string({'list': [1, 2, 3]}) == 'list=1&list=2&list=3'
    assert build_query_string({'mixed': [1, 'two', None]}) == 'mixed=1&mixed=two'

def test_build_query_string_boundary_cases():
    assert build_query_string({'empty': ''}) == 'empty='
    assert build_query_string({'none': None}) == ''
    assert build_query_string({'none': None}, exclude_none=False) == 'none='
    assert build_query_string({'bool': True, 'none': None}, exclude_none=False) == 'bool=true&none='

def test_build_query_string_edge_cases():
    assert build_query_string({}, sort_keys=True) == ''
    assert build_query_string({'single': 'value'}) == 'single=value'
    assert build_query_string({'key': [None, 'value', 'another']}) == 'key=value&key=another'
    assert build_query_string({'key': [None, None]}, exclude_none=False) == 'key=&key='
    assert build_query_string({'key': [None, None]}, exclude_none=True) == ''
    assert build_query_string({'key': [1, 2, 3]}, encode_spaces=False) == 'key=1&key=2&key=3'