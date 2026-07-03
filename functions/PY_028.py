def fit(self, X, y=None):
        """
        Build a BF Tree for the input data.

        Parameters
        ----------
        X : {array-like, sparse matrix} of shape (n_samples, n_features)
            Input data.

        y : Ignored
            Not used, present here for API consistency by convention.

        Returns
        -------
        self
            Fitted estimator.
        """

        # TODO: Add input verification
        return self._fit(X, partial=False)