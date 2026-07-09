import pytest

def test_normalize_path_none_path():
    with pytest.raises(ValueError, match="path is required"):
        normalize_path(None)

def test_normalize_path_empty_path_allow_empty():
    result = normalize_path(None, allow_empty=True)
    assert result == ""

def test_normalize_path_empty_path_not_allow_empty():
    with pytest.raises(ValueError, match="path is required"):
        normalize_path(None)

def test_normalize_path_relative_path_without_base():
    result = normalize_path("folder/file")
    assert result == "/folder/file"

def test_normalize_path_relative_path_with_base():
    result = normalize_path("folder/file", base="/base")
    assert result == "/base/folder/file"

def test_normalize_path_absolute_path():
    result = normalize_path("/folder/file")
    assert result == "/folder/file"

def test_normalize_path_with_dot():
    result = normalize_path("folder/./file")
    assert result == "/folder/file"

def test_normalize_path_with_double_dot():
    result = normalize_path("folder/../file")
    assert result == "/file"

def test_normalize_path_with_double_dot_strict():
    result = normalize_path("folder/../file", strict=True)
    assert result == "/file"

def test_normalize_path_with_double_dot_strict_no_clean():
    result = normalize_path("folder/../..", strict=True)
    assert result == "/.."

def test_normalize_path_with_multiple_double_dots():
    result = normalize_path("folder/../../file", strict=False)
    assert result == "/file"

def test_normalize_path_with_leading_slash():
    result = normalize_path("/folder/file")
    assert result == "/folder/file"

def test_normalize_path_with_trailing_slash():
    result = normalize_path("folder/file/")
    assert result == "/folder/file"

def test_normalize_path_with_empty_parts():
    result = normalize_path("folder//file")
    assert result == "/folder/file"

def test_normalize_path_with_multiple_dots():
    result = normalize_path("folder/././file")
    assert result == "/folder/file"