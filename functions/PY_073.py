def trim_front(strings):
    """
    Trims zeros and decimal points.
    """
    trimmed = strings
    while len(strings) > 0 and all(x[0] == ' ' for x in trimmed):
        trimmed = [x[1:] for x in trimmed]
    return trimmed