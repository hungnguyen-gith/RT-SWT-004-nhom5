def chi(clusters, reps = False, rep_type = "centroid", curated = False, min_size = 1):
    """Calinski-Harabasz index
    
    clusters : list of np.arrays containing the clusters
    
    reps : {bool, list} indicates if cluster representatives are given
    
    rep_type : type of representative, medoid or centroid
    
    curated : bool indicates if singletons have been removed
    
    min_size : int size below which clusters will be ignored
    
    Note
    ----
    Higher values are better
    
    """
    # n : total number of points
    n = 0
    
    # k : number of clusters
    k = len(clusters)
    
    # wcss : within-cluster sum of squares
    wcss = 0
    
    # bcss : between-cluster sum of squares
    bcss = 0
    
    if not curated:
        clusters = remove_singles(clusters, min_size)
    
    total_data = []
    for clust in clusters:
        for mol in clust:
            total_data.append(mol)
    total_data = np.array(total_data)
    if rep_type == 'centroid':
        linear_sum = np.sum(total_data, axis=0)
        n_samples = len(total_data)
        c = calculate_centroid(linear_sum, n_samples)
    elif rep_type == 'medoid':
        medoid = calculate_medoid(total_data)
        c = total_data[medoid]
    
    if not reps:
        for clust in clusters:
            n_samples = len(clust)
            n += n_samples
            if rep_type == 'centroid':
                linear_sum = np.sum(clust, axis=0)
                rep = calculate_centroid(linear_sum, n_samples)
            elif rep_type == 'medoid':
                medoid = calculate_medoid(clust)
                rep = clust[medoid]
            distances = 1 - jt_one_to_many(rep, clust)
            wcss += np.dot(distances, distances)
            bcss += n_samples * (1 - jt_pair(c, rep))**2
    else:
        for i, clust in enumerate(clusters):
            n_samples = len(clust)
            n += n_samples
            bcss += n_samples * (1 - jt_pair(c, reps[i]))**2
            distances = 1 - jt_one_to_many(reps[i], clust)
            wcss += np.dot(distances, distances)
    
    try:
        value = bcss * (n - k)/(wcss * (k - 1))
    except:
        value = 0
    return value