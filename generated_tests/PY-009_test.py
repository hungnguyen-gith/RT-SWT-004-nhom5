import pytest

class TestLoadFunction:
    def test_load_with_valid_path(self):
        result = load(path="valid/path/to/data", format="parquet")
        assert result is not None

    def test_load_with_valid_path_and_schema(self):
        result = load(path="valid/path/to/data", format="parquet", schema="col0 INT, col1 DOUBLE")
        assert result is not None

    def test_load_with_default_format(self):
        result = load(path="valid/path/to/data")
        assert result is not None

    def test_load_with_empty_path(self):
        with pytest.raises(ValueError, match="If the path is provided for stream, it needs to be a non-empty string. List of paths are not supported."):
            load(path="", format="parquet")

    def test_load_with_non_string_path(self):
        with pytest.raises(ValueError, match="If the path is provided for stream, it needs to be a non-empty string. List of paths are not supported."):
            load(path=123, format="parquet")

    def test_load_with_none_path(self):
        result = load()
        assert result is not None

    def test_load_with_whitespace_path(self):
        with pytest.raises(ValueError, match="If the path is provided for stream, it needs to be a non-empty string. List of paths are not supported."):
            load(path="   ", format="parquet")

    def test_load_with_large_path(self):
        long_path = "a" * 1000  # Assuming this is a valid path length
        result = load(path=long_path, format="parquet")
        assert result is not None

    def test_load_with_special_characters_in_path(self):
        result = load(path="valid/path/with/special@chars!", format="parquet")
        assert result is not None

    def test_load_with_invalid_format(self):
        with pytest.raises(ValueError):
            load(path="valid/path/to/data", format="invalid_format")