def _split_node(node, threshold, branching_factor, singly):
    """The node has to be split if there is no place for a new subcluster
    in the node.
    1. Two empty nodes and two empty subclusters are initialized.
    2. The pair of distant subclusters are found.
    3. The properties of the empty subclusters and nodes are updated
       according to the nearest distance between the subclusters to the
       pair of distant subclusters.
    4. The two nodes are set as children to the two subclusters.
    """
    new_subcluster1 = _BFSubcluster()
    new_subcluster2 = _BFSubcluster()
    new_node1 = _BFNode(
        threshold=threshold,
        branching_factor=branching_factor,
        is_leaf=node.is_leaf,
        n_features=node.n_features,
        dtype=node.init_centroids_.dtype,
    )
    new_node2 = _BFNode(
        threshold=threshold,
        branching_factor=branching_factor,
        is_leaf=node.is_leaf,
        n_features=node.n_features,
        dtype=node.init_centroids_.dtype,
    )
    new_subcluster1.child_ = new_node1
    new_subcluster2.child_ = new_node2

    if node.is_leaf:
        if node.prev_leaf_ is not None:
            node.prev_leaf_.next_leaf_ = new_node1
        new_node1.prev_leaf_ = node.prev_leaf_
        new_node1.next_leaf_ = new_node2
        new_node2.prev_leaf_ = new_node1
        new_node2.next_leaf_ = node.next_leaf_
        if node.next_leaf_ is not None:
            node.next_leaf_.prev_leaf_ = new_node2  
    
    # O(N) implementation of max separation
    farthest_idx, node1_dist, node2_dist = max_separation(node.centroids_)    
    # Notice that max_separation is returning similarities and not distances
    node1_closer = node1_dist > node2_dist
    # Make sure node1 is closest to itself even if all distances are equal.
    # This can only happen when all node.centroids_ are duplicates leading to all
    # distances between centroids being zero.
    node1_closer[farthest_idx[0]] = True

    for idx, subcluster in enumerate(node.subclusters_):
        if node1_closer[idx]:
            new_node1.append_subcluster(subcluster)
            new_subcluster1.update(subcluster)
            if not singly:
                subcluster.parent_ = new_subcluster1
        else:
            new_node2.append_subcluster(subcluster)
            new_subcluster2.update(subcluster)
            if not singly:
                subcluster.parent_ = new_subcluster2
    return new_subcluster1, new_subcluster2