import pytest

def test_parse_csv_line_normal_cases():
    assert parse_csv_line("a,b,c") == ["a", "b", "c"]
    assert parse_csv_line("1,2,3") == ["1", "2", "3"]
    assert parse_csv_line("name,age,city") == ["name", "age", "city"]
    assert parse_csv_line("apple,banana,orange") == ["apple", "banana", "orange"]

def test_parse_csv_line_with_quotes():
    assert parse_csv_line('"a,b",c') == ['a,b', 'c']
    assert parse_csv_line('"a","b","c"') == ['a', 'b', 'c']
    assert parse_csv_line('"a, b", "c, d"') == ['a, b', 'c, d']
    assert parse_csv_line('"a""b",c') == ['a"b', 'c']

def test_parse_csv_line_with_delimiter():
    assert parse_csv_line("a|b|c", delimiter="|") == ["a", "b", "c"]
    assert parse_csv_line("1|2|3", delimiter="|") == ["1", "2", "3"]

def test_parse_csv_line_trim_whitespace():
    assert parse_csv_line("  a , b , c  ", trim_whitespace=True) == ["a", "b", "c"]
    assert parse_csv_line("  a ,  b ,  c  ", trim_whitespace=True) == ["a", "b", "c"]

def test_parse_csv_line_skip_empty():
    assert parse_csv_line("a,,c", skip_empty=True) == ["a", "c"]
    assert parse_csv_line(",,", skip_empty=True) == []
    assert parse_csv_line("a,b,,d", skip_empty=True) == ["a", "b", "d"]

def test_parse_csv_line_boundary_cases():
    assert parse_csv_line("") == []
    assert parse_csv_line(",", skip_empty=True) == []
    assert parse_csv_line(",", skip_empty=False) == ["", ""]

def test_parse_csv_line_edge_cases():
    assert parse_csv_line('"a,b",,c', skip_empty=True) == ['a,b', 'c']
    assert parse_csv_line('"",b,c', skip_empty=True) == ['b', 'c']
    assert parse_csv_line('a,"b,c",d', skip_empty=False) == ['a', 'b,c', 'd']