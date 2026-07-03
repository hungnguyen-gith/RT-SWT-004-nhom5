def get_cluster_mol_ids(self):
        """Method to return the indices of molecules in each cluster"""
        # TODO: create torch version of this function for tensor output
        if self.first_call:
            raise ValueError('The model has not been fitted yet.')

        clusters_mol_id = []
        for leaf in self._get_leaves():
            for subcluster in leaf.subclusters_:
                clusters_mol_id.append(subcluster.mol_indices)

        return clusters_mol_id