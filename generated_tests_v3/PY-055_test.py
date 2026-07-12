from functions.PY_055 import normalize_path
import pytest

def test_normalize_path_with_absolute_path():
    assert normalize_path("/a/b/c") == "/a/b/c"

def test_normalize_path_with_relative_path():
    assert normalize_path("b/c", base="/a") == "/a/b/c"

def test_normalize_path_with_dot_segments():
    assert normalize_path("/a/./b/c/./") == "/a/b/c"

def test_normalize_path_with_double_dot_segments():
    assert normalize_path("/a/b/../c") == "/a/c"

def test_normalize_path_with_strict_mode():
    assert normalize_path("/a/b/../c", strict=True) == "/a/c"
    assert normalize_path("/a/b/../..", strict=True) == "/"

def test_normalize_path_with_non_strict_mode():
    assert normalize_path("/a/b/../c", strict=False) == "/a/c"
    assert normalize_path("/a/b/../..", strict=False) == "/a"

def test_normalize_path_with_empty_path_and_allow_empty():
    assert normalize_path(None, allow_empty=True) == ""

def test_normalize_path_with_empty_path_and_no_allow_empty():
    with pytest.raises(ValueError, match="path is required"):
        normalize_path(None)

def test_normalize_path_with_base_and_no_slash():
    assert normalize_path("b/c", base="/a") == "/a/b/c"

def test_normalize_path_with_base_and_leading_slash():
    assert normalize_path("/b/c", base="/a") == "/b/c"

def test_normalize_path_with_multiple_slashes():
    assert normalize_path("//a//b//c//") == "/a/b/c"

def test_normalize_path_with_only_double_dots():
    assert normalize_path("..") == "/"

def test_normalize_path_with_only_dots():
    assert normalize_path(".") == "/"