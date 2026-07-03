def get_centroids_mol_ids(self):
        """Method to return a dictionary containing the centroids and mol indices of the leaves"""
        if self.first_call:
            raise ValueError('The model has not been fitted yet.')
        
        centroids = []
        mol_ids = []
        for leaf in self._get_leaves():
            for subcluster in leaf.subclusters_:
                centroids.append(subcluster.centroid_)
                mol_ids.append(subcluster.mol_indices)

        dict_centroids_mol_ids = {'centroids': centroids, 'mol_ids': mol_ids}

        return dict_centroids_mol_ids