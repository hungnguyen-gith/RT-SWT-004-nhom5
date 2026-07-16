import pytest

class DocSpan:
    def __init__(self, start, length):
        self.start = start
        self.length = length

def check_is_max_context(doc_spans, cur_span_index, position):
    best_score = None
    best_span_index = None
    for (span_index, doc_span) in enumerate(doc_spans):
        end = doc_span.start + doc_span.length - 1
        if position < doc_span.start:
            continue
        if position > end:
            continue
        num_left_context = position - doc_span.start
        num_right_context = end - position
        score = min(num_left_context, num_right_context) + 0.01 * doc_span.length
        if best_score is None or score > best_score:
            best_score = score
            best_span_index = span_index
    return cur_span_index == best_span_index

def test_check_is_max_context():
    # Normal test cases
    assert check_is_max_context([DocSpan(0, 5), DocSpan(5, 5)], 0, 2) == True
    assert check_is_max_context([DocSpan(0, 5), DocSpan(5, 5)], 1, 7) == True
    assert check_is_max_context([DocSpan(0, 5), DocSpan(5, 5)], 0, 4) == False

    # Boundary test cases
    assert check_is_max_context([DocSpan(0, 5)], 0, 0) == True
    assert check_is_max_context([DocSpan(0, 5)], 0, 4) == True
    assert check_is_max_context([DocSpan(0, 5)], 0, 5) == False  # position is out of bounds

    # Edge cases
    assert check_is_max_context([], 0, 0) == False  # No spans
    assert check_is_max_context([DocSpan(0, 1)], 0, 0) == True  # Single span, position at start
    assert check_is_max_context([DocSpan(0, 1)], 0, 1) == False  # Single span, position at end
    assert check_is_max_context([DocSpan(0, 10), DocSpan(10, 10)], 1, 15) == True  # Multiple spans, max context
    assert check_is_max_context([DocSpan(0, 10), DocSpan(10, 10)], 0, 5) == False  # Multiple spans, not max context