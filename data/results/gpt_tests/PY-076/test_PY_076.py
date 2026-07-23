import pytest

def preprocess_sgm(line, is_sgm):
    """Preprocessing to strip tags in SGM files."""
    if not is_sgm:
        return line
    if line.startswith("<srcset") or line.startswith("</srcset"):
        return ""
    if line.startswith("<doc") or line.startswith("</doc"):
        return ""
    if line.startswith("<p>") or line.startswith("</p>"):
        return ""
    line = line.strip()
    if line.startswith("<seg") and line.endswith("</seg>"):
        i = line.index(">")
        return line[i + 1:-6]
    return line

def test_preprocess_sgm_normal_cases():
    assert preprocess_sgm("<srcset ...>", True) == ""
    assert preprocess_sgm("</srcset>", True) == ""
    assert preprocess_sgm("<doc ...>", True) == ""
    assert preprocess_sgm("</doc>", True) == ""
    assert preprocess_sgm("<p>", True) == ""
    assert preprocess_sgm("</p>", True) == ""
    assert preprocess_sgm("<seg>content</seg>", True) == "content"
    assert preprocess_sgm("Some text", False) == "Some text"

def test_preprocess_sgm_boundary_cases():
    assert preprocess_sgm("<seg></seg>", True) == ""
    assert preprocess_sgm("<seg> </seg>", True) == ""
    assert preprocess_sgm("<seg>  content  </seg>", True) == "  content  "
    assert preprocess_sgm("<seg>content</seg> extra", True) == "extra"

def test_preprocess_sgm_edge_cases():
    assert preprocess_sgm("", True) == ""
    assert preprocess_sgm("<seg>", True) == "<seg>"
    assert preprocess_sgm("</seg>", True) == "</seg>"
    assert preprocess_sgm("<srcset ...> some text </srcset>", True) == ""
    assert preprocess_sgm("<doc> some text </doc>", True) == ""
    assert preprocess_sgm("<p> some text </p>", True) == ""
    assert preprocess_sgm("<seg>content</seg> more content", True) == " more content"