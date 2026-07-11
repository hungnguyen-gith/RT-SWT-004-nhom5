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

@inherit_doc
class TestChild(Child):
    pass

@inherit_doc
class TestAnotherChild(AnotherChild):
    pass

def test_inherit_doc_child_method_one():
    assert TestChild.method_one.__doc__ == "This is method one in Child."

def test_inherit_doc_child_method_two():
    assert TestChild.method_two.__doc__ == "This is method two in Parent."

def test_inherit_doc_another_child_method_three():
    assert TestAnotherChild.method_three.__doc__ is None

def test_inherit_doc_no_methods():
    class EmptyClass:
        pass

    @inherit_doc
    class TestEmptyClass(EmptyClass):
        pass

    assert TestEmptyClass.__doc__ is None

def test_inherit_doc_private_method():
    class PrivateParent:
        def _private_method(self):
            """This is a private method in Parent."""
            pass

    @inherit_doc
    class TestPrivateChild(PrivateParent):
        def _private_method(self):
            pass  # No docstring

    assert TestPrivateChild._private_method.__doc__ is None

def test_inherit_doc_multiple_parents():
    class ParentA:
        def method_a(self):
            """This is method A in ParentA."""
            pass

    class ParentB:
        def method_a(self):
            """This is method A in ParentB."""
            pass

    class MultiChild(ParentA, ParentB):
        def method_a(self):
            pass  # No docstring

    @inherit_doc
    class TestMultiChild(MultiChild):
        pass

    assert TestMultiChild.method_a.__doc__ == "This is method A in ParentA."