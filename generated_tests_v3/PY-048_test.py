from functions.PY_048 import get_fk_many_from_list

class Stub:
    def __init__(self, **kwargs):
        self.__dict__.update(kwargs)

    def get(self, key):
        return self.__dict__.get(key)

class FkManyClass:
    update_from_object_fields = ['name']

def test_get_fk_many_from_list_update_existing_fks():
    object_list = [{'id': 1, 'name': 'Object 1'}, {'id': 2, 'name': 'Object 2'}]
    fkmany = [Stub(id=1, name='Old Object 1'), Stub(id=3, name='Old Object 3')]
    key_attr = 'id'

    result = get_fk_many_from_list(Stub(), object_list, fkmany, FkManyClass, key_attr)

    assert len(result) == 3
    assert result[0].name == 'Object 1'
    assert result[1].name == 'Old Object 3'
    assert result[2].name == 'Object 2'

def test_get_fk_many_from_list_create_new_fks():
    object_list = [{'id': 1, 'name': 'Object 1'}, {'id': 2, 'name': 'Object 2'}]
    fkmany = [Stub(id=1, name='Old Object 1')]
    key_attr = 'id'

    result = get_fk_many_from_list(Stub(), object_list, fkmany, FkManyClass, key_attr)

    assert len(result) == 2
    assert result[0].name == 'Old Object 1'
    assert result[1].name == 'Object 2'

def test_get_fk_many_from_list_remove_deleted_fks():
    object_list = [{'id': 1, 'name': 'Object 1'}]
    fkmany = [Stub(id=1, name='Old Object 1'), Stub(id=2, name='Old Object 2')]
    key_attr = 'id'

    result = get_fk_many_from_list(Stub(), object_list, fkmany, FkManyClass, key_attr)

    assert len(result) == 1
    assert result[0].name == 'Old Object 1'

def test_get_fk_many_from_list_empty_object_list():
    object_list = []
    fkmany = [Stub(id=1, name='Old Object 1')]
    key_attr = 'id'

    result = get_fk_many_from_list(Stub(), object_list, fkmany, FkManyClass, key_attr)

    assert len(result) == 0

def test_get_fk_many_from_list_no_fks():
    object_list = [{'id': 1, 'name': 'Object 1'}]
    fkmany = []
    key_attr = 'id'

    result = get_fk_many_from_list(Stub(), object_list, fkmany, FkManyClass, key_attr)

    assert len(result) == 1
    assert result[0].name == 'Object 1'

def test_get_fk_many_from_list_invalid_key_attr():
    object_list = [{'id': 1, 'name': 'Object 1'}]
    fkmany = [Stub(id=1, name='Old Object 1')]
    key_attr = 'invalid_key'

    result = get_fk_many_from_list(Stub(), object_list, fkmany, FkManyClass, key_attr)

    assert len(result) == 1
    assert result[0].name == 'Old Object 1'  # No change should occur

def test_get_fk_many_from_list_partial_update_fields():
    object_list = [{'id': 1, 'name': 'Object 1', 'description': 'A description'}]
    fkmany = [Stub(id=1, name='Old Object 1')]
    key_attr = 'id'

    result = get_fk_many_from_list(Stub(), object_list, fkmany, FkManyClass, key_attr)

    assert len(result) == 1
    assert result[0].name == 'Object 1'  # Should update name
    assert not hasattr(result[0], 'description')  # Should not have description attribute

def test_get_fk_many_from_list_with_additional_fields():
    object_list = [{'id': 1, 'name': 'Object 1', 'extra_field': 'Extra Value'}]
    fkmany = [Stub(id=1, name='Old Object 1')]
    key_attr = 'id'

    result = get_fk_many_from_list(Stub(), object_list, fkmany, FkManyClass, key_attr)

    assert len(result) == 1
    assert result[0].name == 'Object 1'  # Should update name
    assert not hasattr(result[0], 'extra_field')  # Should not have extra_field attribute