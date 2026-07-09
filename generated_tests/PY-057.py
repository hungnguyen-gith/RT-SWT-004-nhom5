import pytest

def test_parse_csv_line_basic():
    assert parse_csv_line("a,b,c") == ["a", "b", "c"]

def test_parse_csv_line_with_quotes():
    assert parse_csv_line('"a,b",c') == ['a,b', 'c']

def test_parse_csv_line_with_empty_fields():
    assert parse_csv_line("a,,c") == ["a", "", "c"]

def test_parse_csv_line_with_trimming():
    assert parse_csv_line("  a , b , c  ", trim_whitespace=True) == ["a", "b", "c"]

def test_parse_csv_line_with_skip_empty():
    assert parse_csv_line("a,,c", skip_empty=True) == ["a", "c"]

def test_parse_csv_line_with_quotes_and_empty_fields():
    assert parse_csv_line('"a,b",,c') == ['a,b', '', 'c']

def test_parse_csv_line_with_double_quotes():
    assert parse_csv_line('"a""b",c') == ['a"b', 'c']

def test_parse_csv_line_with_custom_delimiter():
    assert parse_csv_line("a|b|c", delimiter="|") == ["a", "b", "c"]

def test_parse_csv_line_with_trim_and_skip_empty():
    assert parse_csv_line("  a , , c  ", trim_whitespace=True, skip_empty=True) == ["a", "c"]

def test_parse_csv_line_with_only_empty_fields():
    assert parse_csv_line(",,", skip_empty=True) == []