def fit_BFs(self, X):
        """
        Method to fit a BitBirch model with the given BitFeatyres.

        Parameters:
        -----------
        X : list of BitFeatures

        Returns:
        --------
        self
        """

        # Check that the input is a list of BitFeatures
        if type(X) != list or len(X[0]) != 3:
            raise ValueError('The input must be a list of BitFeatures')
        
        threshold = self.threshold
        branching_factor = self.branching_factor

        n_features = len(X[0][1])
        d_type = X[0][1].dtype

        # If partial_fit is called for the first time or fit is called, we
        # start a new tree.
        if self.first_call:
            # The first root is the leaf. Manipulate this object throughout.
            self.root_ = _BFNode(
                threshold=threshold,
                branching_factor=branching_factor,
                is_leaf=True,
                n_features=n_features,
                dtype=d_type,
            )
    
            # To enable getting back subclusters.
            self.dummy_leaf_ = _BFNode(
                threshold=threshold,
                branching_factor=branching_factor,
                is_leaf=True,
                n_features=n_features,
                dtype=d_type,
            )
            self.dummy_leaf_.next_leaf_ = self.root_
            self.root_.prev_leaf_ = self.dummy_leaf_

        for sample in iter(X):

            cluster = _BFSubcluster()
            cluster.n_samples_, cluster.linear_sum_, cluster.mol_indices = sample[0], sample[1], sample[2]
            cluster.centroid_ = calc_centroid(cluster.linear_sum_, cluster.n_samples_)

            set_bits = np.sum(cluster.centroid_)
            split = self.root_.insert_bf_subcluster(cluster, set_bits, cluster.parent_, True)

            if split:
                new_subcluster1, new_subcluster2 = _split_node(
                    self.root_, threshold, branching_factor, True
                )
                del self.root_
                self.root_ = _BFNode(
                    threshold=threshold,
                    branching_factor=branching_factor,
                    is_leaf=False,
                    n_features=n_features,
                    dtype=d_type,
                )
                self.root_.append_subcluster(new_subcluster1)
                self.root_.append_subcluster(new_subcluster2)
            self.index_tracker += 1

        centroids = np.concatenate([leaf.centroids_ for leaf in self._get_leaves()])
        self.subcluster_centers_ = centroids
        self._n_features_out = self.subcluster_centers_.shape[0]
        
        self.first_call = False
        return self