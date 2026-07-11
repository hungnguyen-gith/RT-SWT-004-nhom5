def getitem_block(self, slicer, new_mgr_locs=None):
        """
        Perform __getitem__-like, return result as block.

        As of now, only supports slices that preserve dimensionality.
        """
        if new_mgr_locs is None:
            if isinstance(slicer, tuple):
                axis0_slicer = slicer[0]
            else:
                axis0_slicer = slicer
            new_mgr_locs = self.mgr_locs[axis0_slicer]

        new_values = self._slice(slicer)

        if self._validate_ndim and new_values.ndim != self.ndim:
            raise ValueError("Only same dim slicing is allowed")

        return self.make_block_same_class(new_values, new_mgr_locs)