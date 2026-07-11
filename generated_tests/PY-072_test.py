import pytest

class TestStartFunction:
    def test_start_with_default_parameters(self):
        result = self.start()
        assert result is not None
        assert result.isActive is False

    def test_start_with_path(self):
        result = self.start(path='/some/path')
        assert result is not None
        assert result.isActive is False

    def test_start_with_format(self):
        result = self.start(format='json')
        assert result is not None
        assert result.isActive is False

    def test_start_with_output_mode_append(self):
        result = self.start(outputMode='append')
        assert result is not None
        assert result.isActive is False

    def test_start_with_output_mode_complete(self):
        result = self.start(outputMode='complete')
        assert result is not None
        assert result.isActive is False

    def test_start_with_output_mode_update(self):
        result = self.start(outputMode='update')
        assert result is not None
        assert result.isActive is False

    def test_start_with_partition_by(self):
        result = self.start(partitionBy=['column1', 'column2'])
        assert result is not None
        assert result.isActive is False

    def test_start_with_query_name(self):
        result = self.start(queryName='test_query')
        assert result is not None
        assert result.isActive is False

    def test_start_with_all_parameters(self):
        result = self.start(path='/some/path', format='parquet', outputMode='append', 
                            partitionBy=['column1'], queryName='test_query')
        assert result is not None
        assert result.isActive is False

    def test_start_with_none_path(self):
        result = self.start(path=None)
        assert result is not None
        assert result.isActive is False

    def test_start_with_empty_string_path(self):
        result = self.start(path='')
        assert result is not None
        assert result.isActive is False

    def test_start_with_invalid_output_mode(self):
        with pytest.raises(ValueError):
            self.start(outputMode='invalid_mode')

    def test_start_with_large_partition_by(self):
        result = self.start(partitionBy=['col' + str(i) for i in range(1000)])
        assert result is not None
        assert result.isActive is False

    def test_start_with_special_characters_in_query_name(self):
        result = self.start(queryName='test_query_!@#$%^&*()')
        assert result is not None
        assert result.isActive is False