def is_uniform_join_units(join_units):
    """
    Check if the join units consist of blocks of uniform type that can
    be concatenated using Block.concat_same_type instead of the generic
    concatenate_join_units (which uses `_concat._concat_compat`).

    """
    return (
        # all blocks need to have the same type
        all(type(ju.block) is type(join_units[0].block) for ju in join_units) and  # noqa
        # no blocks that would get missing values (can lead to type upcasts)
        # unless we're an extension dtype.
        all(not ju.is_na or ju.block.is_extension for ju in join_units) and
        # no blocks with indexers (as then the dimensions do not fit)
        all(not ju.indexers for ju in join_units) and
        # disregard Panels
        all(ju.block.ndim <= 2 for ju in join_units) and
        # only use this path when there is something to concatenate
        len(join_units) > 1)