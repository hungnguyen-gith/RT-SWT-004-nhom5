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
    assert normalize_path("/a/b/c/") == "/a/b/c"
    assert normalize_path("/a/b/c/..") == "/a/b"
    assert normalize_path("/..") == "/"
    assert normalize_path("/a/../..") == "/"
    assert normalize_path("..", "/base") == "/base/.."

def test_edge_cases():
    with pytest.raises(ValueError, match="path is required"):
        normalize_path(None)
    assert normalize_path("..", strict=True) == "/"
    assert normalize_path("..", strict=False) == "/.."
    assert normalize_path("/a/b/c/../../d") == "/d"
    assert normalize_path("/./././") == "/"
    assert normalize_path("/a/b/c", strict=True) == "/a/b/c"