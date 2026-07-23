import pytest

class TestGetFunction:
    def setup_method(self):
        self.obj = YourClass()  # Replace with the actual class name
        self.obj._conf = {'key1': 'value1', 'key2': 'value2'}
        self.obj._jconf = None  # or set it to a mock object if needed

    def test_get_existing_key(self):
        assert self.obj.get('key1') == 'value1'

    def test_get_non_existing_key(self):
        assert self.obj.get('key3') is None

    def test_get_with_default_value_existing_key(self):
        assert self.obj.get('key1', 'default') == 'value1'

    def test_get_with_default_value_non_existing_key(self):
        assert self.obj.get('key3', 'default') == 'default'

    def test_get_with_none_default_value_existing_key(self):
        assert self.obj.get('key1', None) == 'value1'

    def test_get_with_none_default_value_non_existing_key(self):
        assert self.obj.get('key3', None) is None

    def test_get_with_jconf_existing_key(self):
        self.obj._jconf = MockJConf({'key1': 'jconf_value1'})
        assert self.obj.get('key1') == 'jconf_value1'

    def test_get_with_jconf_non_existing_key(self):
        self.obj._jconf = MockJConf({'key1': 'jconf_value1'})
        assert self.obj.get('key2') is None

    def test_get_with_jconf_and_default_value_existing_key(self):
        self.obj._jconf = MockJConf({'key1': 'jconf_value1'})
        assert self.obj.get('key1', 'default') == 'jconf_value1'

    def test_get_with_jconf_and_default_value_non_existing_key(self):
        self.obj._jconf = MockJConf({'key1': 'jconf_value1'})
        assert self.obj.get('key2', 'default') == 'default'

    def test_get_with_empty_conf(self):
        self.obj._conf = {}
        assert self.obj.get('key1') is None

    def test_get_with_empty_jconf(self):
        self.obj._jconf = MockJConf({})
        assert self.obj.get('key1') is None

class MockJConf:
    def __init__(self, data):
        self.data = data

    def contains(self, key):
        return key in self.data

    def get(self, key, default=None):
        return self.data.get(key, default)