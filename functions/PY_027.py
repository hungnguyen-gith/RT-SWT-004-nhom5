def merge_subcluster(self, nominee_cluster, threshold):
        """Check if a cluster is worthy enough to be merged. If
        yes then merge.
        """
        new_ls = self.linear_sum_ + nominee_cluster.linear_sum_
        new_n = self.n_samples_ + nominee_cluster.n_samples_
        new_centroid = calc_centroid(new_ls, new_n)
        
        # TODO: Incorporate other criteria for merging
        # multiply 2 instead of div

        ls_cent=new_ls+new_centroid
        jt_radius = jt_isim(ls_cent, new_n + 1) * (new_n + 1) - jt_isim(new_ls, new_n) * (new_n - 1)
        
        if jt_radius >= threshold*2:
            (
                self.n_samples_,
                self.linear_sum_,
                self.centroid_,
                self.mol_indices,
            ) = (new_n, new_ls, new_centroid, self.mol_indices + nominee_cluster.mol_indices)

            return True
        return False