from functions.PY_054 import build_query_string

def test_build_query_string_normal_cases():
    params = {'name': 'John Doe', 'age': 30, 'active': True}
    result = build_query_string(params)
    assert result == 'active=true&age=30&name=John+Doe'

    params = {'name': 'Alice', 'hobbies': ['reading', 'traveling'], 'age': None}
    result = build_query_string(params)
    assert result == 'hobbies=reading&hobbies=traveling&name=Alice'

def test_build_query_string_exclude_none():
    params = {'name': 'John Doe', 'age': None, 'active': True}
    result = build_query_string(params, exclude_none=True)
    assert result == 'active=true&name=John+Doe'

    result = build_query_string(params, exclude_none=False)
    assert result == 'active=true&age=&name=John+Doe'

def test_build_query_string_sort_keys():
    params = {'b': 2, 'a': 1, 'c': 3}
    result = build_query_string(params, sort_keys=True)
    assert result == 'a=1&b=2&c=3'

def test_build_query_string_encode_spaces():
    params = {'name': 'John Doe', 'address': '123 Main St'}
    result = build_query_string(params, encode_spaces=True)
    assert result == 'address=123+Main+St&name=John+Doe'

    result = build_query_string(params, encode_spaces=False)
    assert result == 'address=123 Main St&name=John Doe'

def test_build_query_string_with_lists():
    params = {'tags': ['python', 'pytest', 'testing']}
    result = build_query_string(params)
    assert result == 'tags=python&tags=pytest&tags=testing'

def test_build_query_string_with_empty_params():
    params = {}
    result = build_query_string(params)
    assert result == ''

def test_build_query_string_with_boolean_values():
    params = {'is_active': True, 'is_verified': False}
    result = build_query_string(params)
    assert result == 'is_active=true&is_verified=false'

def test_build_query_string_with_none_values():
    params = {'key1': None, 'key2': None}
    result = build_query_string(params)
    assert result == ''

def test_build_query_string_with_mixed_types():
    params = {'key1': 'value1', 'key2': None, 'key3': [1, 2, 3], 'key4': True}
    result = build_query_string(params)
    assert result == 'key1=value1&key3=1&key3=2&key3=3&key4=true'