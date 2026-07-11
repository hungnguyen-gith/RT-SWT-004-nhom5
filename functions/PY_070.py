def construction_error(tot_items, block_shape, axes, e=None):
    """ raise a helpful message about our construction """
    passed = tuple(map(int, [tot_items] + list(block_shape)))
    # Correcting the user facing error message during dataframe construction
    if len(passed) <= 2:
        passed = passed[::-1]

    implied = tuple(len(ax) for ax in axes)
    # Correcting the user facing error message during dataframe construction
    if len(implied) <= 2:
        implied = implied[::-1]

    if passed == implied and e is not None:
        raise e
    if block_shape[0] == 0:
        raise ValueError("Empty data passed with indices specified.")
    raise ValueError("Shape of passed values is {0}, indices imply {1}".format(
        passed, implied))