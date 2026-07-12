import pytest

# Sample classes for testing
class Parent:
    def method_one(self):
        """This is method one in Parent."""
        pass

    def method_two(self):
        """This is method two in Parent."""
        pass

class Child(Parent):
    def method_one(self):
        """This is method one in Child."""
        pass

    def method_two(self):
        pass  # No docstring

class AnotherChild(Parent):
    def method_three(self):
        pass  # No docstring

@pytest.fixture
def decorated_child():
    return inherit_doc(Child)

@pytest.fixture
def decorated_another_child():
    return inherit_doc(AnotherChild)

def test_inherit_doc_decorated_child_method_one(decorated_child):
    assert decorated_child.method_one.__doc__ == "This is method one in Child."

def test_inherit_doc_decorated_child_method_two(decorated_child):
    assert decorated_child.method_two.__doc__ == "This is method two in Parent."

def test_inherit_doc_decorated_another_child_method_three(decorated_another_child):
    assert decorated_another_child.method_three.__doc__ is None

def test_inherit_doc_no_methods():
    class NoMethods:
        pass

    decorated_no_methods = inherit_doc(NoMethods)
    assert not vars(decorated_no_methods)

def test_inherit_doc_private_method():
    class PrivateMethodClass(Parent):
        def _private_method(self):
            pass  # No docstring

    decorated_private = inherit_doc(PrivateMethodClass)
    assert decorated_private._private_method.__doc__ is None

def test_inherit_doc_multiple_parents():
    class ParentA:
        def method(self):
            """Doc from ParentA"""
            pass

    class ParentB:
        def method(self):
            """Doc from ParentB"""
            pass

    class ChildMultiple(ParentA, ParentB):
        def method(self):
            pass  # No docstring

    decorated_child_multiple = inherit_doc(ChildMultiple)
    assert decorated_child_multiple.method.__doc__ == "Doc from ParentA"