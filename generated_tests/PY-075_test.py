import pytest

class TestGetCorpusLine:
    class MockCorpus:
        def __init__(self, corpus_lines, on_memory, all_docs, sample_to_doc):
            self.corpus_lines = corpus_lines
            self.on_memory = on_memory
            self.all_docs = all_docs
            self.sample_to_doc = sample_to_doc
            self.line_buffer = None
            self.current_doc = 0

        def get_corpus_line(self, item):
            # Function implementation here...

    def test_normal_case_on_memory(self):
        all_docs = {
            0: ["line1_doc0", "line2_doc0"],
            1: ["line1_doc1", "line2_doc1"]
        }
        sample_to_doc = [{ "doc_id": 0, "line": 0 }, { "doc_id": 1, "line": 0 }]
        corpus = self.MockCorpus(2, True, all_docs, sample_to_doc)
        assert corpus.get_corpus_line(0) == ("line1_doc0", "line2_doc0")
        assert corpus.get_corpus_line(1) == ("line1_doc1", "line2_doc1")

    def test_normal_case_not_on_memory(self):
        all_docs = {
            0: ["line1_doc0", "line2_doc0"],
            1: ["line1_doc1", "line2_doc1"]
        }
        corpus = self.MockCorpus(2, False, all_docs, [])
        corpus.file = iter(["line1_doc0", "line2_doc0", "line1_doc1", "line2_doc1"])
        assert corpus.get_corpus_line(0) == ("line1_doc0", "line2_doc0")
        assert corpus.get_corpus_line(1) == ("line1_doc1", "line2_doc1")

    def test_boundary_case(self):
        all_docs = {
            0: ["line1_doc0", "line2_doc0"],
        }
        sample_to_doc = [{ "doc_id": 0, "line": 0 }]
        corpus = self.MockCorpus(1, True, all_docs, sample_to_doc)
        assert corpus.get_corpus_line(0) == ("line1_doc0", "line2_doc0")

    def test_edge_case_empty_lines(self):
        all_docs = {
            0: ["", "line2_doc0"],
            1: ["line1_doc1", ""]
        }
        sample_to_doc = [{ "doc_id": 0, "line": 0 }, { "doc_id": 1, "line": 0 }]
        corpus = self.MockCorpus(2, True, all_docs, sample_to_doc)
        assert corpus.get_corpus_line(0) == ("", "line2_doc0")
        assert corpus.get_corpus_line(1) == ("line1_doc1", "")

    def test_out_of_bounds(self):
        all_docs = {
            0: ["line1_doc0", "line2_doc0"],
        }
        sample_to_doc = [{ "doc_id": 0, "line": 0 }]
        corpus = self.MockCorpus(1, True, all_docs, sample_to_doc)
        with pytest.raises(AssertionError):
            corpus.get_corpus_line(1)

    def test_empty_corpus(self):
        all_docs = {}
        sample_to_doc = []
        corpus = self.MockCorpus(0, True, all_docs, sample_to_doc)
        with pytest.raises(AssertionError):
            corpus.get_corpus_line(0)