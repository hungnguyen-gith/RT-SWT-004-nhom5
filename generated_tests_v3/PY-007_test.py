from functions.PY_007 import get
import pytest

class Stub:
    def __init__(self, jconf=None, conf=None):
        self._jconf = jconf
        self._conf = conf or {}

class MockJConf:
    def __init__(self, data):
        self.data = data

    def contains(self, key):
        return key in self.data

    def get(self, key, default=None):
        return self.data.get(key, default)

def test_get_with_jconf_key_exists():
    jconf = MockJConf({'key1': 'value1'})
    stub = Stub(jconf=jconf)
    assert get(stub, 'key1') == 'value1'

def test_get_with_jconf_key_not_exists():
    jconf = MockJConf({'key1': 'value1'})
    stub = Stub(jconf=jconf)
    assert get(stub, 'key2') is None

def test_get_with_jconf_key_exists_with_default():
    jconf = MockJConf({'key1': 'value1'})
    stub = Stub(jconf=jconf)
    assert get(stub, 'key2', 'default_value') == 'default_value'

def test_get_with_jconf_none():
    stub = Stub(jconf=None, conf={'key1': 'value1'})
    assert get(stub, 'key1') == 'value1'

def test_get_with_jconf_none_key_not_exists():
    stub = Stub(jconf=None, conf={'key1': 'value1'})
    assert get(stub, 'key2') is None

def test_get_with_jconf_none_key_exists_with_default():
    stub = Stub(jconf=None, conf={'key1': 'value1'})
    assert get(stub, 'key2', 'default_value') == 'default_value'

def test_get_with_default_value_none_and_jconf_key_exists():
    jconf = MockJConf({'key1': 'value1'})
    stub = Stub(jconf=jconf)
    assert get(stub, 'key1', None) == 'value1'

def test_get_with_default_value_none_and_jconf_key_not_exists():
    jconf = MockJConf({'key1': 'value1'})
    stub = Stub(jconf=jconf)
    assert get(stub, 'key2', None) is None

def test_get_with_default_value_none_and_conf_key_exists():
    stub = Stub(jconf=None, conf={'key1': 'value1'})
    assert get(stub, 'key1', None) == 'value1'

def test_get_with_default_value_none_and_conf_key_not_exists():
    stub = Stub(jconf=None, conf={'key1': 'value1'})
    assert get(stub, 'key2', None) is None

def test_get_with_default_value_provided():
    stub = Stub(jconf=None, conf={'key1': 'value1'})
    assert get(stub, 'key2', 'default_value') == 'default_value'