from functions.PY_008 import inherit_doc

class BaseClass:
    """Base class documentation."""

    def base_method(self):
        """Base method documentation."""
        pass

class DerivedClass(BaseClass):
    """Derived class documentation."""

    def derived_method(self):
        """Derived method documentation."""
        pass

    def another_method(self):
        pass  # No docstring

def test_inherit_doc_with_documented_method():
    @inherit_doc
    class TestClass(DerivedClass):
        pass

    assert TestClass.base_method.__doc__ == "Base method documentation."
    assert TestClass.derived_method.__doc__ == "Derived method documentation."

def test_inherit_doc_without_documented_method():
    @inherit_doc
    class TestClass(DerivedClass):
        def another_method(self):
            pass  # No docstring

    assert TestClass.another_method.__doc__ is None

def test_inherit_doc_with_multiple_bases():
    class AnotherBase:
        """Another base class documentation."""

        def another_base_method(self):
            """Another base method documentation."""
            pass

    class CombinedClass(AnotherBase, BaseClass):
        pass

    @inherit_doc
    class TestClass(CombinedClass):
        def another_base_method(self):
            pass  # No docstring

    assert TestClass.another_base_method.__doc__ == "Another base method documentation."
    assert TestClass.base_method.__doc__ == "Base method documentation."

def test_inherit_doc_with_private_method():
    @inherit_doc
    class TestClass(DerivedClass):
        def _private_method(self):
            """Private method documentation."""
            pass

    assert TestClass._private_method.__doc__ is None

def test_inherit_doc_with_no_bases():
    @inherit_doc
    class TestClass:
        pass

    assert TestClass.__doc__ is None

def test_inherit_doc_with_non_callable_attributes():
    class NonCallable:
        pass

    @inherit_doc
    class TestClass(NonCallable):
        pass

    assert TestClass.__doc__ is None

def test_inherit_doc_with_empty_docstrings():
    class EmptyDocBase:
        """ """
        
        def empty_method(self):
            """ """
            pass

    @inherit_doc
    class TestClass(EmptyDocBase):
        def another_method(self):
            pass  # No docstring

    assert TestClass.empty_method.__doc__ == ""  # Changed to check for empty string
    assert TestClass.another_method.__doc__ is None