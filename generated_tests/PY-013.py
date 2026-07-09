import pytest

# Mocking the jt_isim function for testing purposes
def jt_isim(ls, n):
    return sum(ls) / n if n > 0 else 0

# The function to be tested
def merge_accept(threshold, new_ls, new_centroid, new_n, old_ls, nom_ls, old_n, nom_n):
    jt_radius = jt_isim(new_ls, new_n)
    if jt_radius < threshold:
        return False
    else:
        if old_n == 1 and nom_n == 1:
            return True
        elif nom_n == 1:
            return (jt_isim(old_ls + nom_ls, old_n + 1) * (old_n + 1) - jt_isim(old_ls, old_n) * (old_n - 1)) / 2 >= jt_isim(old_ls, old_n) - 0.1 and (jt_radius >= threshold)
        else:
            return (jt_isim(old_ls + nom_ls, old_n + nom_n) * (old_n + nom_n) * (old_n + nom_n - 1) 
                    - jt_isim(old_ls, old_n) * old_n * (old_n - 1)
                    - jt_isim(nom_ls, nom_n) * nom_n * (nom_n - 1)) / (2 * old_n * nom_n) >= jt_isim(old_ls, old_n) - 0.1 and (jt_radius >= threshold)

# Test cases
def test_merge_accept():
    assert merge_accept(0.5, [1, 2], None, 2, [1], [1], 1, 1) == True
    assert merge_accept(0.5, [1, 2], None, 2, [1], [2], 1, 1) == False
    assert merge_accept(0.5, [1, 2], None, 2, [1, 2], [1], 2, 1) == True
    assert merge_accept(0.5, [1, 2], None, 2, [1, 2], [2, 3], 2, 2) == True
    assert merge_accept(0.5, [1, 2], None, 2, [1, 2], [3], 2, 1) == False
    assert merge_accept(0.5, [1, 2], None, 2, [1, 2], [1, 2], 2, 2) == True
    assert merge_accept(0.5, [1, 2], None, 2, [1, 2], [1], 2, 1) == False
    assert merge_accept(0.5, [1, 2], None, 2, [1, 2], [1, 2], 2, 1) == False
    assert merge_accept(0.5, [1, 2], None, 2, [1, 2], [3, 4], 2, 2) == True
    assert merge_accept(0.5, [1, 2], None, 2, [1, 2], [], 2, 0) == False