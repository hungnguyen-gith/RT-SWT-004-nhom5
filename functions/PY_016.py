def reindex_indexer(self, new_axis, indexer, axis, fill_value=None,
                        allow_dups=False, copy=True):
        """
        Parameters
        ----------
        new_axis : Index
        indexer : ndarray of int64 or None
        axis : int
        fill_value : object
        allow_dups : bool

        pandas-indexer with -1's only.
        """
        if indexer is None:
            if new_axis is self.axes[axis] and not copy:
                return self

            result = self.copy(deep=copy)
            result.axes = list(self.axes)
            result.axes[axis] = new_axis
            return result

        self._consolidate_inplace()

        # some axes don't allow reindexing with dups
        if not allow_dups:
            self.axes[axis]._can_reindex(indexer)

        if axis >= self.ndim:
            raise IndexError("Requested axis not found in manager")

        if axis == 0:
            new_blocks = self._slice_take_blocks_ax0(indexer,
                                                     fill_tuple=(fill_value,))
        else:
            new_blocks = [blk.take_nd(indexer, axis=axis, fill_tuple=(
                fill_value if fill_value is not None else blk.fill_value,))
                for blk in self.blocks]

        new_axes = list(self.axes)
        new_axes[axis] = new_axis
        return self.__class__(new_blocks, new_axes)
