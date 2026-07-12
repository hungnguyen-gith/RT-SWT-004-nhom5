from functions.PY_081 import trigger
import pytest

class Stub:
    def __init__(self):
        self._spark = StubSpark()
        self._jwrite = StubJWrite()

class StubSpark:
    def __init__(self):
        self._sc = StubSc()

class StubSc:
    def __init__(self):
        self._jvm = StubJvm()

class StubJvm:
    def __init__(self):
        self.org = StubOrg()

class StubOrg:
    def __init__(self):
        self.apache = StubApache()

class StubApache:
    def __init__(self):
        self.spark = StubSparkModule()

class StubSparkModule:
    class sql:
        class streaming:
            class Trigger:
                @staticmethod
                def ProcessingTime(interval):
                    return f"ProcessingTime({interval})"

                @staticmethod
                def Once():
                    return "Once()"

                @staticmethod
                def Continuous(interval):
                    return f"Continuous({interval})"

class StubJWrite:
    def trigger(self, jTrigger):
        return f"Triggered with {jTrigger}"

def test_trigger_processing_time():
    stub = Stub()
    result = trigger(stub, processingTime='5 seconds')
    assert result._jwrite.trigger(result._jwrite.trigger("ProcessingTime(5 seconds)")) == "Triggered with ProcessingTime(5 seconds)"

def test_trigger_once():
    stub = Stub()
    result = trigger(stub, once=True)
    assert result._jwrite.trigger(result._jwrite.trigger("Once()")) == "Triggered with Once()"

def test_trigger_continuous():
    stub = Stub()
    result = trigger(stub, continuous='10 seconds')
    assert result._jwrite.trigger(result._jwrite.trigger("Continuous(10 seconds)")) == "Triggered with Continuous(10 seconds)"

def test_trigger_no_parameters():
    stub = Stub()
    with pytest.raises(ValueError, match='No trigger provided'):
        trigger(stub)

def test_trigger_multiple_parameters():
    stub = Stub()
    with pytest.raises(ValueError, match='Multiple triggers not allowed.'):
        trigger(stub, processingTime='5 seconds', once=True)

def test_trigger_invalid_processing_time_type():
    stub = Stub()
    with pytest.raises(ValueError, match='Value for processingTime must be a non empty string. Got: 123'):
        trigger(stub, processingTime=123)

def test_trigger_empty_processing_time():
    stub = Stub()
    with pytest.raises(ValueError, match='Value for processingTime must be a non empty string. Got: '):
        trigger(stub, processingTime='')

def test_trigger_invalid_once_value():
    stub = Stub()
    with pytest.raises(ValueError, match='Value for once must be True. Got: False'):
        trigger(stub, once=False)

def test_trigger_invalid_continuous_type():
    stub = Stub()
    with pytest.raises(ValueError, match='Value for continuous must be a non empty string. Got: 123'):
        trigger(stub, continuous=123)

def test_trigger_empty_continuous():
    stub = Stub()
    with pytest.raises(ValueError, match='Value for continuous must be a non empty string. Got: '):
        trigger(stub, continuous='')