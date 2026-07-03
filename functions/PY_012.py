def reassign(self, X, top=20, quick=False):
        """
        Reassign molecules across the user-specified (default 20) top largest clusters in the tree based on the tanimoto similarity matrix. 

        Parameters
        ----------
        X : {array-like, sparse matrix} of shape (n_samples, n_features)
            Input data.

        top: int
            default: 20; specifies number of top largest clusters to reassign

        quick: boolean
            default: False; if quick specifed, the whole tree will not be return, but a dictionary of top cluster data will be returned

        Return
        ------
        quick return: dict
            dictionary sorted by largest to smallest newly reassigned top clusters

        self
            Fitted estimator.
        """
        top_clusters, centroids, mol_indices, data_top_clusters = self._get_top_cluster_params(X, top)
        row_max = self._get_sim_matrix(data_top_clusters, centroids)


        final_clusters = {i: [] for i in np.unique(row_max)}
        for mol, cluster_idx in zip(mol_indices, row_max):
            final_clusters[cluster_idx].append(mol)
        
        if quick:
            return dict(sorted(final_clusters.items(), key=lambda item: len(item[1]), reverse=True))    #Return dict sorted by largest to smallest newly reassigned top clusters
        
        else:
            sub_clusters = [sc for leaf in self._get_leaves() for sc in leaf.subclusters_]
            assert len(sub_clusters) == len(self.get_cluster_mol_ids())
           
            top_sub_clusters = sorted(sub_clusters, key=lambda c: c.n_samples_, reverse=True)[:top]
   
            for sc, tc in zip(top_sub_clusters, top_clusters):
                assert sc.n_samples_ == len(tc)

            for cluster, c_ids in zip(top_sub_clusters, final_clusters.values()):
                cluster.n_samples_ = len(c_ids)
                cluster.linear_sum = np.sum(X[c_ids], axis=0)
                cluster.mol_indices = c_ids
                cluster.centroid_ = calc_centroid(cluster.linear_sum_, cluster.n_samples_)
        return self