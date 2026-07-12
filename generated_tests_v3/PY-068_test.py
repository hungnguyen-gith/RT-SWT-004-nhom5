from functions.PY_068 import check_is_max_context

class DocSpan:
    def __init__(self, start, length):
        self.start = start
        self.length = length

def test_check_is_max_context():
    # Test case 1: Normal case where the max context is the last span
    doc_spans = [DocSpan(0, 5), DocSpan(5, 5), DocSpan(10, 5)]
    assert check_is_max_context(doc_spans, 2, 12) is True

    # Test case 2: Normal case where the max context is the first span
    doc_spans = [DocSpan(0, 5), DocSpan(5, 5), DocSpan(10, 5)]
    assert check_is_max_context(doc_spans, 0, 2) is True

    # Test case 3: Normal case where the max context is the middle span
    doc_spans = [DocSpan(0, 5), DocSpan(5, 5), DocSpan(10, 5)]
    assert check_is_max_context(doc_spans, 1, 7) is True

    # Test case 4: Edge case where position is before the first span
    doc_spans = [DocSpan(0, 5), DocSpan(5, 5)]
    assert check_is_max_context(doc_spans, 0, -1) is False

    # Test case 5: Edge case where position is after the last span
    doc_spans = [DocSpan(0, 5), DocSpan(5, 5)]
    assert check_is_max_context(doc_spans, 1, 12) is False

    # Test case 6: Edge case where position is exactly at the start of a span
    doc_spans = [DocSpan(0, 5), DocSpan(5, 5)]
    assert check_is_max_context(doc_spans, 1, 5) is True

    # Test case 7: Edge case where position is exactly at the end of a span
    doc_spans = [DocSpan(0, 5), DocSpan(5, 5)]
    assert check_is_max_context(doc_spans, 0, 4) is True

    # Test case 8: Multiple spans with the same context score
    doc_spans = [DocSpan(0, 5), DocSpan(5, 5), DocSpan(10, 5)]
    assert check_is_max_context(doc_spans, 1, 6) is True  # Both span 1 and 2 have the same score

    # Test case 9: Single span case
    doc_spans = [DocSpan(0, 5)]
    assert check_is_max_context(doc_spans, 0, 2) is True
    assert check_is_max_context(doc_spans, 0, 0) is True
    assert check_is_max_context(doc_spans, 0, 4) is True
    assert check_is_max_context(doc_spans, 0, 5) is False  # Out of bounds

    # Test case 10: Invalid input case (empty spans)
    doc_spans = []
    assert check_is_max_context(doc_spans, 0, 2) is False  # No spans to check against