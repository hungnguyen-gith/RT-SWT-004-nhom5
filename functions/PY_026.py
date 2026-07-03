def insert_bf_subcluster(self, subcluster):
        """Insert a new subcluster into the node."""
        if not self.subclusters_:
            self.append_subcluster(subcluster)
            return False

        threshold = self.threshold
        branching_factor = self.branching_factor
        # We need to find the closest subcluster among all the
        # subclusters so that we can insert our new subcluster.

        a = np.dot(self.centroids_, subcluster.centroid_)
        sim_matrix = self.centroids_sum[0][:len(self.centroids_)] / a # inverse 
        closest_index = np.argmin(sim_matrix) # inverse
        closest_subcluster = self.subclusters_[closest_index]

        # If the subcluster has a child, we need a recursive strategy.
        if closest_subcluster.child_ is not None:
            split_child = closest_subcluster.child_.insert_bf_subcluster(subcluster)

            if not split_child:
                # If it is determined that the child need not be split, we
                # can just update the closest_subcluster
                closest_subcluster.update(subcluster)
                temp=self.subclusters_[closest_index].centroid_
                self.init_centroids_[closest_index] = temp
                self.centroids_[closest_index] = temp
                self.centroids_sum[0, closest_index] = np.sum(temp)
                return False

            # things not too good. we need to redistribute the subclusters in
            # our child node, and add a new subcluster in the parent
            # subcluster to accommodate the new child.
            else:
                new_subcluster1, new_subcluster2 = _split_node(
                    closest_subcluster.child_,
                    threshold,
                    branching_factor
                )
                self.update_split_subclusters(
                    closest_index, new_subcluster1, new_subcluster2
                )

                if len(self.subclusters_) > self.branching_factor:
                    return True
                return False

        # good to go!
        else:
            merged = closest_subcluster.merge_subcluster(subcluster, self.threshold)
            if merged:
                temp=closest_subcluster.centroid_
 
                self.centroids_[closest_index]=temp             
                self.init_centroids_[closest_index] = temp
                self.centroids_sum[0, closest_index] = np.sum(temp)

                return False

            # not close to any other subclusters, and we still
            # have space, so add.
            elif len(self.subclusters_) < self.branching_factor:
                self.append_subcluster(subcluster)
                return False

            # We do not have enough space nor is it closer to an
            # other subcluster. We need to split.
            else:
                self.append_subcluster(subcluster)
                return True