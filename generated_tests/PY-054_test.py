import pytest

def test_build_query_string_normal_cases():
    assert build_query_string({'a': 1, 'b': 2}) == 'a=1&b=2'
    assert build_query_string({'name': 'John Doe', 'age': 30}) == 'age=30&name=John+Doe'
    assert build_query_string({'key': None, 'value': 'test'}, exclude_none=False) == 'key=&value=test'
    assert build_query_string({'key': None, 'value': 'test'}) == 'value=test'

def test_build_query_string_sort_keys():
    assert build_query_string({'b': 2, 'a': 1}) == 'a=1&b=2'
    assert build_query_string({'c': 3, 'a': 1, 'b': 2}) == 'a=1&b=2&c=3'

def test_build_query_string_with_booleans():
    assert build_query_string({'is_active': True, 'is_deleted': False}) == 'is_active=true&is_deleted=false'

def test_build_query_string_with_lists():
    assert build_query_string({'ids': [1, 2, 3]}) == 'ids=1&ids=2&ids=3'
    assert build_query_string({'tags': ['python', 'pytest']}) == 'tags=python&tags=pytest'

def test_build_query_string_exclude_none():
    assert build_query_string({'key1': None, 'key2': 'value2'}) == 'key2=value2'
    assert build_query_string({'key1': None, 'key2': None}, exclude_none=False) == 'key1=&key2='

def test_build_query_string_encode_spaces():
    assert build_query_string({'name': 'John Doe', 'city': 'New York'}) == 'city=New+York&name=John+Doe'
    assert build_query_string({'name': 'John Doe', 'city': 'New York'}, encode_spaces=False) == 'city=New York&name=John Doe'

def test_build_query_string_empty_params():
    assert build_query_string({}) == ''

def test_build_query_string_boundary_cases():
    assert build_query_string({'key': ''}) == 'key='
    assert build_query_string({'key': 0}) == 'key=0'
    assert build_query_string({'key': False}) == 'key=false'

def test_build_query_string_edge_cases():
    assert build_query_string({'key': [None, 'value']}) == 'key=value'
    assert build_query_string({'key': [None, None]}) == ''
    assert build_query_string({'key': [True, False]}) == 'key=true&key=false'