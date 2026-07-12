from functions.PY_075 import get_corpus_line
import pytest

class Stub:
    def __init__(self, corpus_lines, on_memory, sample_to_doc, all_docs, line_buffer=None, file=None):
        self.corpus_lines = corpus_lines
        self.on_memory = on_memory
        self.sample_to_doc = sample_to_doc
        self.all_docs = all_docs
        self.line_buffer = line_buffer
        self.file = file
        self.current_doc = 0

def test_get_corpus_line_on_memory():
    stub = Stub(
        corpus_lines=2,
        on_memory=True,
        sample_to_doc=[{"doc_id": 0, "line": 0}, {"doc_id": 0, "line": 1}],
        all_docs={0: ["First line.", "Second line."]}
    )
    result = get_corpus_line(stub, 0)
    assert result == ("First line.", "Second line.")

def test_get_corpus_line_on_memory_edge_case():
    stub = Stub(
        corpus_lines=1,
        on_memory=True,
        sample_to_doc=[{"doc_id": 0, "line": 0}],
        all_docs={0: ["Only line."]}
    )
    result = get_corpus_line(stub, 0)
    assert result == ("Only line.", "")

def test_get_corpus_line_file_mode():
    from io import StringIO

    file_content = "First line.\nSecond line.\n\nThird line.\nFourth line."
    file = StringIO(file_content)
    
    stub = Stub(
        corpus_lines=4,
        on_memory=False,
        sample_to_doc=[],
        all_docs=[],
        line_buffer=None,
        file=file
    )

    result1 = get_corpus_line(stub, 0)
    assert result1 == ("First line.", "Second line.")

    result2 = get_corpus_line(stub, 1)
    assert result2 == ("Second line.", "Third line.")

def test_get_corpus_line_empty_lines():
    from io import StringIO

    file_content = "First line.\n\nSecond line.\n\nThird line."
    file = StringIO(file_content)

    stub = Stub(
        corpus_lines=3,
        on_memory=False,
        sample_to_doc=[],
        all_docs=[],
        line_buffer=None,
        file=file
    )

    result1 = get_corpus_line(stub, 0)
    assert result1 == ("First line.", "Second line.")

    result2 = get_corpus_line(stub, 1)
    assert result2 == ("Second line.", "Third line.")

def test_get_corpus_line_invalid_index():
    stub = Stub(
        corpus_lines=2,
        on_memory=True,
        sample_to_doc=[{"doc_id": 0, "line": 0}],
        all_docs={0: ["First line."]}
    )
    with pytest.raises(AssertionError):
        get_corpus_line(stub, 2)

def test_get_corpus_line_empty_file():
    from io import StringIO

    file_content = "\n\n"
    file = StringIO(file_content)

    stub = Stub(
        corpus_lines=2,
        on_memory=False,
        sample_to_doc=[],
        all_docs=[],
        line_buffer=None,
        file=file
    )

    with pytest.raises(AssertionError):
        get_corpus_line(stub, 0)