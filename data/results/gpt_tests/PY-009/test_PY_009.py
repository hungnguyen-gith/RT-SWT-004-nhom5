import pytest

class TestLoadFunction:
    def test_load_with_valid_path(self):
        result = load(path="valid/path/to/data", format="parquet")
        assert result is not None  # Assuming the function returns a DataFrame

    def test_load_with_default_format(self):
        result = load(path="valid/path/to/data")
        assert result is not None

    def test_load_with_schema(self):
        result = load(path="valid/path/to/data", schema="col0 INT, col1 DOUBLE")
        assert result is not None

    def test_load_with_options(self):
        result = load(path="valid/path/to/data", options={"option1": "value1"})
        assert result is not None

    def test_load_with_empty_path(self):
        with pytest.raises(ValueError, match="If the path is provided for stream, it needs to be a non-empty string. List of paths are not supported."):
            load(path="")

    def test_load_with_non_string_path(self):
        with pytest.raises(ValueError, match="If the path is provided for stream, it needs to be a non-empty string. List of paths are not supported."):
            load(path=123)

    def test_load_with_none_path(self):
        result = load()
        assert result is not None

    def test_load_with_whitespace_path(self):
        with pytest.raises(ValueError, match="If the path is provided for stream, it needs to be a non-empty string. List of paths are not supported."):
            load(path="   ")

    def test_load_with_large_schema(self):
        schema = ", ".join([f"col{i} STRING" for i in range(1000)])  # Large schema
        result = load(path="valid/path/to/data", schema=schema)
        assert result is not None

    def test_load_with_special_characters_in_path(self):
        result = load(path="valid/path/to/data/with special@chars!")
        assert result is not None