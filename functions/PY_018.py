def dbi(clusters, reps = False, rep_type = "centroid", curated = False, min_size = 1):
    """Davies-Bouldin index
    
    clusters : list of np.arrays containing the clusters
    
    reps : {bool, list} indicates if cluster representatives are given
    
    rep_type : type of representative, medoid or centroid
    
    curated : bool indicates if singletons have been removed
    
    min_size : int size below which clusters will be ignored
    
    Note
    ----
    Lower values are better
    
    """
    if not curated:
        clusters = remove_singles(clusters, min_size)
    
    n = 0
    
    S = []
    
    if not reps:
        reps  = []
        for clust in clusters:
            n_samples = len(clust)
            n += n_samples
            if rep_type == 'centroid':
                linear_sum = np.sum(clust, axis=0)
                rep = calculate_centroid(linear_sum, n_samples)
            elif rep_type == 'medoid':
                medoid = calculate_medoid(clust)
                rep = clust[medoid]
            reps.append(rep)
            S.append(np.sum(1 - jt_one_to_many(rep, clust))/n_samples)
    else:
        for i, clust in enumerate(clusters):
            n_samples = len(clust)
            n += n_samples
            S.append(np.sum(1 - jt_one_to_many(reps[i], clust))/n_samples)
    
    db  = 0
    
    for i, clust in enumerate(clusters):
        d = []
        for j, other_clust in enumerate(clusters):
            if i == j:
                d.append(-1)
            else:
                Mij = 1 - jt_pair(reps[i], reps[j])
                Rij = (S[i] + S[j])/Mij
                d.append(Rij)
        db += max(d)
    
    try:
        value = db/n
    except:
        value = 0

    return value