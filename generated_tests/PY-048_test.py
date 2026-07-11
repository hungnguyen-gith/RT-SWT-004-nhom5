import pytest

class MockFKManyClass:
    update_from_object_fields = ['name', 'value']

    def __init__(self, **kwargs):
        for key, value in kwargs.items():
            setattr(self, key, value)

class TestGetFkManyFromList:
    def test_normal_case(self):
        object_list = [{'id': 1, 'name': 'Object1', 'value': 10},
                       {'id': 2, 'name': 'Object2', 'value': 20}]
        fkmany = [MockFKManyClass(id=1, name='OldName', value=5)]
        key_attr = 'id'
        
        result = get_fk_many_from_list(self, object_list, fkmany, MockFKManyClass, key_attr)
        
        assert len(result) == 1
        assert result[0].name == 'Object1'
        assert result[0].value == 10

    def test_boundary_case_empty_lists(self):
        object_list = []
        fkmany = []
        key_attr = 'id'
        
        result = get_fk_many_from_list(self, object_list, fkmany, MockFKManyClass, key_attr)
        
        assert result == []

    def test_boundary_case_one_object(self):
        object_list = [{'id': 1, 'name': 'Object1', 'value': 10}]
        fkmany = []
        key_attr = 'id'
        
        result = get_fk_many_from_list(self, object_list, fkmany, MockFKManyClass, key_attr)
        
        assert len(result) == 1
        assert result[0].name == 'Object1'
        assert result[0].value == 10

    def test_edge_case_removed_fk(self):
        object_list = [{'id': 1, 'name': 'Object1', 'value': 10}]
        fkmany = [MockFKManyClass(id=2, name='OldName', value=5)]
        key_attr = 'id'
        
        result = get_fk_many_from_list(self, object_list, fkmany, MockFKManyClass, key_attr)
        
        assert len(result) == 1
        assert result[0].name == 'Object1'
        assert result[0].value == 10

    def test_edge_case_multiple_new_objects(self):
        object_list = [{'id': 1, 'name': 'Object1', 'value': 10},
                       {'id': 2, 'name': 'Object2', 'value': 20}]
        fkmany = []
        key_attr = 'id'
        
        result = get_fk_many_from_list(self, object_list, fkmany, MockFKManyClass, key_attr)
        
        assert len(result) == 2
        assert result[0].name == 'Object1'
        assert result[1].name == 'Object2'

    def test_edge_case_no_updates(self):
        object_list = [{'id': 1, 'name': 'Object1', 'value': 10}]
        fkmany = [MockFKManyClass(id=1, name='Object1', value=10)]
        key_attr = 'id'
        
        result = get_fk_many_from_list(self, object_list, fkmany, MockFKManyClass, key_attr)
        
        assert len(result) == 1
        assert result[0].name == 'Object1'
        assert result[0].value == 10