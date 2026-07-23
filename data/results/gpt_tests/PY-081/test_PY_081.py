import pytest

class TestTrigger:
    def setup_method(self):
        self.mock_spark = type('MockSpark', (), {
            '_sc': type('MockSc', (), {
                '_jvm': type('MockJvm', (), {
                    'org': type('MockOrg', (), {
                        'apache': type('MockApache', (), {
                            'spark': type('MockSpark', (), {
                                'sql': type('MockSql', (), {
                                    'streaming': type('MockStreaming', (), {
                                        'Trigger': type('MockTrigger', (), {
                                            'ProcessingTime': lambda x: f'ProcessingTime({x})',
                                            'Once': lambda: 'Once()',
                                            'Continuous': lambda x: f'Continuous({x})'
                                        })()
                                    })()
                                })()
                            })()
                        })()
                    })()
                })()
            })(),
            '_jwrite': type('MockJWrite', (), {
                'trigger': lambda self, jTrigger: f'Trigger set to {jTrigger}'
            })()
        })()
        self.writer = self.mock_spark

    def test_trigger_processing_time(self):
        result = self.writer.trigger(processingTime='5 seconds')
        assert result == 'Trigger set to ProcessingTime(5 seconds)'

    def test_trigger_once(self):
        result = self.writer.trigger(once=True)
        assert result == 'Trigger set to Once()'

    def test_trigger_continuous(self):
        result = self.writer.trigger(continuous='5 seconds')
        assert result == 'Trigger set to Continuous(5 seconds)'

    def test_no_trigger(self):
        with pytest.raises(ValueError, match='No trigger provided'):
            self.writer.trigger()

    def test_multiple_triggers(self):
        with pytest.raises(ValueError, match='Multiple triggers not allowed.'):
            self.writer.trigger(processingTime='5 seconds', once=True)

    def test_invalid_processing_time_type(self):
        with pytest.raises(ValueError, match='Value for processingTime must be a non empty string. Got: 5'):
            self.writer.trigger(processingTime=5)

    def test_empty_processing_time(self):
        with pytest.raises(ValueError, match='Value for processingTime must be a non empty string. Got: '):
            self.writer.trigger(processingTime='')

    def test_invalid_once_value(self):
        with pytest.raises(ValueError, match='Value for once must be True. Got: False'):
            self.writer.trigger(once=False)

    def test_invalid_continuous_type(self):
        with pytest.raises(ValueError, match='Value for continuous must be a non empty string. Got: 5'):
            self.writer.trigger(continuous=5)

    def test_empty_continuous(self):
        with pytest.raises(ValueError, match='Value for continuous must be a non empty string. Got: '):
            self.writer.trigger(continuous='')