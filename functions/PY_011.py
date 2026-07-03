def _get_top_cluster_params(self, X, top):
        """Method to recieve the cluster mol indices, centroids, and fingerprints of the top user-specified clusters.
        
        Parameters
        ----------
        X : {array-like, sparse matrix} of shape (n_samples, n_features)
            Input data.
        
        top: int
            default: 20; specifies number of top largest clusters to reassign

        Returns
        -------
        top_clusters: sorted list
            list of len top; containing the cluster mol ids of given clusters

        centroids: np.array; shape (top, n_features)
            centroids of the top clusters

        mol_indices: list of indices with the top clusters; len of number of molecules in all top clusters

        data_top_clusters: np.array; shape (n_molecules, n_features)
            fingerprints of the molecules in the top clusters
        """
        top_clusters = sorted(self.get_cluster_mol_ids(), key=len, reverse=True)[:top]
        centroids = np.array([self._calc_centroid(X, c) for c in top_clusters])
        mol_indices = [i for c in top_clusters for i in c]
        data_top_clusters = np.array([X[i] for i in mol_indices])
        assert data_top_clusters.shape[0] == len(mol_indices)

        return top_clusters, centroids, mol_indices, data_top_clusters