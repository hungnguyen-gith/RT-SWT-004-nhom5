def get_BFs(self):
        """Method to return the BitFeatures of the leaves"""
        if self.first_call:
            raise ValueError('The model has not been fitted yet.')
        
        BFs = []
        for leaf in self._get_leaves():
            for subcluster in leaf.subclusters_:
                BFs.append(subcluster)

        # Sort the BitFeatures by the number of samples in the cluster
        BFs = sorted(BFs, key = lambda x: x.n_samples_, reverse = True)

        return BFs