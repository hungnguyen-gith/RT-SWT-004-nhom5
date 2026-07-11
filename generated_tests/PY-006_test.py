import pytest

class TestSetExecutorEnv:
    def test_set_single_key_value(self):
        obj = YourClass()  # Replace with your actual class name
        obj.set = lambda k, v: (k, v)  # Mocking the set method
        result = obj.setExecutorEnv(key='TEST_KEY', value='TEST_VALUE')
        assert result == obj
        assert obj.set("spark.executorEnv.TEST_KEY", 'TEST_VALUE') == ("spark.executorEnv.TEST_KEY", 'TEST_VALUE')

    def test_set_multiple_pairs(self):
        obj = YourClass()  # Replace with your actual class name
        obj.set = lambda k, v: (k, v)  # Mocking the set method
        pairs = [('KEY1', 'VALUE1'), ('KEY2', 'VALUE2')]
        result = obj.setExecutorEnv(pairs=pairs)
        assert result == obj
        assert obj.set("spark.executorEnv.KEY1", 'VALUE1') == ("spark.executorEnv.KEY1", 'VALUE1')
        assert obj.set("spark.executorEnv.KEY2", 'VALUE2') == ("spark.executorEnv.KEY2", 'VALUE2')

    def test_set_both_key_value_and_pairs(self):
        obj = YourClass()  # Replace with your actual class name
        with pytest.raises(Exception, match="Either pass one key-value pair or a list of pairs"):
            obj.setExecutorEnv(key='TEST_KEY', value='TEST_VALUE', pairs=[('KEY1', 'VALUE1')])

    def test_set_neither_key_value_nor_pairs(self):
        obj = YourClass()  # Replace with your actual class name
        with pytest.raises(Exception, match="Either pass one key-value pair or a list of pairs"):
            obj.setExecutorEnv()

    def test_set_empty_pairs(self):
        obj = YourClass()  # Replace with your actual class name
        obj.set = lambda k, v: (k, v)  # Mocking the set method
        result = obj.setExecutorEnv(pairs=[])
        assert result == obj

    def test_set_key_with_none_value(self):
        obj = YourClass()  # Replace with your actual class name
        obj.set = lambda k, v: (k, v)  # Mocking the set method
        result = obj.setExecutorEnv(key='TEST_KEY', value=None)
        assert result == obj
        assert obj.set("spark.executorEnv.TEST_KEY", None) == ("spark.executorEnv.TEST_KEY", None)

    def test_set_key_with_empty_string_value(self):
        obj = YourClass()  # Replace with your actual class name
        obj.set = lambda k, v: (k, v)  # Mocking the set method
        result = obj.setExecutorEnv(key='TEST_KEY', value='')
        assert result == obj
        assert obj.set("spark.executorEnv.TEST_KEY", '') == ("spark.executorEnv.TEST_KEY", '')