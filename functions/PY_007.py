def get_cluster_mol_ids(self):
        """Method to return the indices of molecules in each cluster"""
        if self.first_call:
            raise ValueError('The model has not been fitted yet.')
        
        clusters_mol_id = []
        for leaf in self._get_leaves():
            for subcluster in leaf.subclusters_:
                clusters_mol_id.append(subcluster.mol_indices)

        # Sort the clusters by the number of samples in the cluster
        clusters_mol_id = sorted(clusters_mol_id, key = lambda x: len(x), reverse = True)

        return clusters_mol_id