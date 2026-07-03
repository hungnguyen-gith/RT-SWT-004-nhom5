def _get_prune_indices(self):
        """Method to return the indices of molecules in the largest cluster, specifically to be used in fit_reinsert."""
        largest_cluster = max(
            (
                (leaf_idx, cluster_idx, len(cluster.mol_indices))
                for leaf_idx, leaf in enumerate(self._get_leaves())
                for cluster_idx, cluster in enumerate(leaf.subclusters_)
            ),
            key=lambda x: x[2],  # Sort by the cluster size
            default=(None, None, 0),  # Default if no clusters are found
        )
        prune_indices = lazyPrune(largest_cluster[0], largest_cluster[1], self) 
        return prune_indices