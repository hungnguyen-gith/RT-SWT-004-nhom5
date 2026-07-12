from functions.PY_006 import setExecutorEnv
import pytest

class Stub:
    def set(self, key, value):
        # Stub method to simulate the behavior of the real set method
        self.last_key = key
        self.last_value = value

def test_setExecutorEnv_single_key_value():
    stub = Stub()
    key = "MY_VAR"
    value = "my_value"
    result = setExecutorEnv(stub, key, value)
    assert result == stub
    assert stub.last_key == "spark.executorEnv.MY_VAR"
    assert stub.last_value == "my_value"

def test_setExecutorEnv_multiple_pairs():
    stub = Stub()
    pairs = [("VAR1", "value1"), ("VAR2", "value2")]
    result = setExecutorEnv(stub, pairs=pairs)
    assert result == stub
    assert stub.last_key == "spark.executorEnv.VAR2"
    assert stub.last_value == "value2"  # Last pair should be the last set

def test_setExecutorEnv_no_key_value_or_pairs():
    stub = Stub()
    with pytest.raises(Exception, match="Either pass one key-value pair or a list of pairs"):
        setExecutorEnv(stub)

def test_setExecutorEnv_both_key_value_and_pairs():
    stub = Stub()
    key = "MY_VAR"
    value = "my_value"
    pairs = [("VAR1", "value1")]
    with pytest.raises(Exception, match="Either pass one key-value pair or a list of pairs"):
        setExecutorEnv(stub, key, value, pairs=pairs)

def test_setExecutorEnv_key_none_pairs_empty():
    stub = Stub()
    result = setExecutorEnv(stub, pairs=[])
    assert result == stub
    # No keys should be set, so last_key and last_value should not exist
    assert not hasattr(stub, 'last_key')

def test_setExecutorEnv_key_empty_value():
    stub = Stub()
    key = "EMPTY_VAR"
    value = ""
    result = setExecutorEnv(stub, key, value)
    assert result == stub
    assert stub.last_key == "spark.executorEnv.EMPTY_VAR"
    assert stub.last_value == ""  # Check if empty value is handled correctly

def test_setExecutorEnv_pairs_with_empty_values():
    stub = Stub()
    pairs = [("VAR1", ""), ("VAR2", None)]
    result = setExecutorEnv(stub, pairs=pairs)
    assert result == stub
    assert stub.last_key == "spark.executorEnv.VAR2"
    assert stub.last_value is None  # Check if None value is handled correctly