from functions.PY_057 import parse_csv_line

class Stub:
    pass

def test_parse_csv_line_normal():
    stub = Stub()
    assert parse_csv_line('a,b,c') == ['a', 'b', 'c']
    assert parse_csv_line('a,"b,c",d') == ['a', 'b,c', 'd']
    assert parse_csv_line('"a,b",c,d') == ['a,b', 'c', 'd']

def test_parse_csv_line_with_delimiter():
    stub = Stub()
    assert parse_csv_line('a|b|c', delimiter='|') == ['a', 'b', 'c']
    assert parse_csv_line('a|b|c|', delimiter='|') == ['a', 'b', 'c', '']
    assert parse_csv_line('a|b|c|', delimiter='|', skip_empty=True) == ['a', 'b', 'c']

def test_parse_csv_line_with_quotes():
    stub = Stub()
    assert parse_csv_line('"a|b"|c|d', delimiter='|') == ['a|b', 'c', 'd']
    assert parse_csv_line('"a|b|c|d"', delimiter='|') == ['a|b|c|d']

def test_parse_csv_line_trim_whitespace():
    stub = Stub()
    assert parse_csv_line('  a , b , c  ', trim_whitespace=True) == ['a', 'b', 'c']
    assert parse_csv_line('  a ,  , c  ', trim_whitespace=True, skip_empty=True) == ['a', 'c']

def test_parse_csv_line_empty_input():
    stub = Stub()
    assert parse_csv_line('') == ['']
    assert parse_csv_line('', skip_empty=True) == []

def test_parse_csv_line_invalid_input():
    stub = Stub()
    assert parse_csv_line('a,b,c', delimiter='|') == ['a,b,c']
    assert parse_csv_line('a,"b,c', delimiter=',') == ['a', 'b,c']
    assert parse_csv_line('"a,b",c,"d', delimiter=',') == ['a,b', 'c', 'd']

def test_parse_csv_line_multiple_consecutive_delimiters():
    stub = Stub()
    assert parse_csv_line('a,,b', skip_empty=False) == ['a', '', 'b']
    assert parse_csv_line('a,,b', skip_empty=True) == ['a', 'b']
    assert parse_csv_line(',,', skip_empty=True) == []