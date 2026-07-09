import pytest

def test_tokenize_simple_expression_numbers():
    assert tokenize_simple_expression("123") == [("NUMBER", "123")]
    assert tokenize_simple_expression("3.14") == [("NUMBER", "3.14")]
    assert tokenize_simple_expression("0.5") == [("NUMBER", "0.5")]
    assert tokenize_simple_expression("42 3.14") == [("NUMBER", "42"), ("NUMBER", "3.14")]

def test_tokenize_simple_expression_identifiers():
    assert tokenize_simple_expression("var") == [("IDENT", "var")]
    assert tokenize_simple_expression("var1") == [("IDENT", "var1")]
    assert tokenize_simple_expression("var_2") == [("IDENT", "var_2")]
    assert tokenize_simple_expression("var1 var2") == [("IDENT", "var1"), ("IDENT", "var2")]

def test_tokenize_simple_expression_operators():
    assert tokenize_simple_expression("+ - * /") == [("OP", "+"), ("OP", "-"), ("OP", "*"), ("OP", "/")]
    assert tokenize_simple_expression("( )") == [("OP", "("), ("OP", ")")]

def test_tokenize_simple_expression_mixed():
    assert tokenize_simple_expression("3 + var") == [("NUMBER", "3"), ("OP", "+"), ("IDENT", "var")]
    assert tokenize_simple_expression("x * 2.5 - (y / 3)") == [("IDENT", "x"), ("OP", "*"), ("NUMBER", "2.5"), ("OP", "-"), ("OP", "("), ("IDENT", "y"), ("OP", "/"), ("NUMBER", "3"), ("OP", ")")]

def test_tokenize_simple_expression_unexpected_character():
    with pytest.raises(ValueError, match="Unexpected character: @"):
        tokenize_simple_expression("3 + @")
    with pytest.raises(ValueError, match="Unexpected character: #"):
        tokenize_simple_expression("#var")
    with pytest.raises(ValueError, match="Unexpected character: $"):
        tokenize_simple_expression("var$")