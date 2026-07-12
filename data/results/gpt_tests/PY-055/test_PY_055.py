import pytest

def test_normalize_path():
    assert normalize_path("/a/b/c") == "/a/b/c"
    assert normalize_path("a/b/c", "/base") == "/base/a/b/c"
    assert normalize_path("/a/b/../c") == "/a/c"
    assert normalize_path("/a/./b/c") == "/a/b/c"
    assert normalize_path("a/b/c", "/base") == "/base/a/b/c"
    assert normalize_path("/a/b/c/", allow_empty=True) == "/a/b/c"
    assert normalize_path("", allow_empty=True) == ""

def test_boundary_cases():
    assert normalize_path("/", allow_empty=True) == "/"
    assert normalize_path("", allow_empty=False) == ""
    with pytest.raises(ValueError):
        normalize_path(None)
    assert normalize_path(None, allow_empty=True) == ""

def test_edge_cases():
    assert normalize_path("..") == "/"
    assert normalize_path("../..") == "/"
    assert normalize_path("/../..") == "/"
    assert normalize_path("/a/b/../../c") == "/c"
    assert normalize_path("/a/b/././c") == "/a/b/c"
    assert normalize_path("..", strict=True) == "/"
    assert normalize_path("..", strict=False) == "/.."