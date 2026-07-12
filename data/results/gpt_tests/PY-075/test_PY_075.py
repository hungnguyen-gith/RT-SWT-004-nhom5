import pytest

class TestGetCorpusLine:
    class MockCorpus:
        def __init__(self, corpus_lines, on_memory, sample_to_doc, all_docs):
            self.corpus_lines = corpus_lines
            self.on_memory = on_memory
            self.sample_to_doc = sample_to_doc
            self.all_docs = all_docs
            self.current_doc = 0
            self.line_buffer = None
            self.file = iter([])  # Placeholder for file iterator

        def get_corpus_line(self, item):
            # Function implementation here...

    def test_normal_case(self):
        corpus = self.MockCorpus(
            corpus_lines=3,
            on_memory=True,
            sample_to_doc=[{"doc_id": 0, "line": 0}, {"doc_id": 0, "line": 1}, {"doc_id": 1, "line": 0}],
            all_docs=[
                ["Line 1.1", "Line 1.2"],
                ["Line 2.1", "Line 2.2"]
            ]
        )
        assert corpus.get_corpus_line(0) == ("Line 1.1", "Line 1.2")
        assert corpus.get_corpus_line(1) == ("Line 1.2", "Line 2.1")

    def test_boundary_case(self):
        corpus = self.MockCorpus(
            corpus_lines=2,
            on_memory=True,
            sample_to_doc=[{"doc_id": 0, "line": 0}, {"doc_id": 1, "line": 0}],
            all_docs=[
                ["Line 1.1", "Line 1.2"],
                ["Line 2.1", "Line 2.2"]
            ]
        )
        assert corpus.get_corpus_line(1) == ("Line 2.1", "Line 2.2")

    def test_edge_case(self):
        corpus = self.MockCorpus(
            corpus_lines=1,
            on_memory=True,
            sample_to_doc=[{"doc_id": 0, "line": 0}],
            all_docs=[
                ["Line 1.1", "Line 1.2"]
            ]
        )
        with pytest.raises(AssertionError):
            corpus.get_corpus_line(1)  # Out of bounds

    def test_empty_lines(self):
        corpus = self.MockCorpus(
            corpus_lines=2,
            on_memory=False,
            sample_to_doc=[],
            all_docs=[],
        )
        corpus.file = iter(["", "Line 1.1", "", "Line 1.2", ""])
        assert corpus.get_corpus_line(0) == ("Line 1.1", "Line 1.2")

    def test_single_line_file(self):
        corpus = self.MockCorpus(
            corpus_lines=1,
            on_memory=False,
            sample_to_doc=[],
            all_docs=[],
        )
        corpus.file = iter(["Line 1.1"])
        with pytest.raises(StopIteration):
            corpus.get_corpus_line(0)  # Not enough lines to return