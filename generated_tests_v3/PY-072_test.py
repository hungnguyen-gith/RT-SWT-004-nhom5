from functions.PY_072 import start
import pytest

class Stub:
    def __init__(self):
        self._jwrite = StubJWrite()
    
    def options(self, **options):
        pass
    
    def outputMode(self, mode):
        assert mode in ["append", "complete", "update"], "Invalid output mode"
    
    def partitionBy(self, partition):
        assert isinstance(partition, list), "partitionBy must be a list"
    
    def format(self, fmt):
        assert fmt in ["csv", "json", "parquet", "memory"], "Invalid format"
    
    def queryName(self, name):
        assert isinstance(name, str), "queryName must be a string"
    
    def _sq(self, value):
        return value

class StubJWrite:
    def start(self, path=None):
        return "Stream started" if path else "Stream started without path"

@pytest.fixture
def stub():
    return Stub()

def test_start_with_path(stub):
    result = start(stub, path="some/path", format="csv", outputMode="append", queryName="test_query")
    assert result == "Stream started"

def test_start_without_path(stub):
    result = start(stub, format="json", outputMode="complete", queryName="test_query")
    assert result == "Stream started without path"

def test_start_with_invalid_output_mode(stub):
    with pytest.raises(AssertionError, match="Invalid output mode"):
        start(stub, outputMode="invalid_mode")

def test_start_with_partition_by(stub):
    start(stub, path="some/path", format="parquet", outputMode="append", partitionBy=["column1", "column2"])
    # No assertion needed, just checking if it runs without error

def test_start_with_invalid_partition_by(stub):
    with pytest.raises(AssertionError, match="partitionBy must be a list"):
        start(stub, path="some/path", format="csv", outputMode="append", partitionBy="not_a_list")

def test_start_with_invalid_format(stub):
    with pytest.raises(AssertionError, match="Invalid format"):
        start(stub, path="some/path", format="invalid_format", outputMode="append")

def test_start_with_query_name(stub):
    start(stub, path="some/path", format="memory", outputMode="update", queryName="my_query")
    # No assertion needed, just checking if it runs without error

def test_start_with_invalid_query_name(stub):
    with pytest.raises(AssertionError, match="queryName must be a string"):
        start(stub, path="some/path", format="json", outputMode="append", queryName=123)