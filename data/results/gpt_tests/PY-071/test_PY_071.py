import pytest

class DummySkeletonClass:
    def __init__(self):
        self.attributes = {}
    
    def __setattr__(self, name, value):
        if name != 'attributes':
            self.attributes[name] = value
        super().__setattr__(name, value)

    def register(self, subclass):
        if 'subclasses' not in self.attributes:
            self.attributes['subclasses'] = []
        self.attributes['subclasses'].append(subclass)

def test_rehydrate_skeleton_class_normal():
    skeleton = DummySkeletonClass()
    class_dict = {'attr1': 'value1', 'attr2': 'value2'}
    
    result = rehydrate_skeleton_class(skeleton, class_dict)
    
    assert result.attributes['attr1'] == 'value1'
    assert result.attributes['attr2'] == 'value2'

def test_rehydrate_skeleton_class_with_registry():
    skeleton = DummySkeletonClass()
    class_dict = {'_abc_impl': ['SubClass1', 'SubClass2'], 'attr1': 'value1'}
    
    result = rehydrate_skeleton_class(skeleton, class_dict)
    
    assert result.attributes['attr1'] == 'value1'
    assert 'SubClass1' in result.attributes['subclasses']
    assert 'SubClass2' in result.attributes['subclasses']

def test_rehydrate_skeleton_class_empty_dict():
    skeleton = DummySkeletonClass()
    class_dict = {}
    
    result = rehydrate_skeleton_class(skeleton, class_dict)
    
    assert result.attributes == {}

def test_rehydrate_skeleton_class_boundary():
    skeleton = DummySkeletonClass()
    class_dict = {'_abc_impl': [], 'attr1': 'value1'}
    
    result = rehydrate_skeleton_class(skeleton, class_dict)
    
    assert result.attributes['attr1'] == 'value1'
    assert 'subclasses' not in result.attributes

def test_rehydrate_skeleton_class_edge_case():
    skeleton = DummySkeletonClass()
    class_dict = {'_abc_impl': None, 'attr1': 'value1'}
    
    result = rehydrate_skeleton_class(skeleton, class_dict)
    
    assert result.attributes['attr1'] == 'value1'
    assert 'subclasses' not in result.attributes

def test_rehydrate_skeleton_class_with_non_string_keys():
    skeleton = DummySkeletonClass()
    class_dict = {123: 'value1', (1, 2): 'value2'}
    
    result = rehydrate_skeleton_class(skeleton, class_dict)
    
    assert result.attributes[123] == 'value1'
    assert result.attributes[(1, 2)] == 'value2'