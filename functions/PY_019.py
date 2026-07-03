def clust_dispersion(clusters, reps = False, rep_type = "centroid", curated = False, min_size = 1):
    """Cluster dispersion
    
    cd = isim(representatives)/<isim(clusters)>
    
    clusters : list of np.arrays containing the clusters
    
    reps : {bool, list} indicates if cluster representatives are given
    
    rep_type : type of representative, medoid or centroid
    
    curated : bool indicates if singletons have been removed
    
    min_size : int size below which clusters will be ignored
    
    Note
    ----
    Lower values are better TODO: DOUBLE CHECK THIS!!!!
    """
    if not curated:
        clusters = remove_singles(clusters, min_size)
    
    n_clusters = len(clusters)
    
    if n_clusters == 1:
        return -1
    
    isim_clusts = 0
    
    if not reps:
        representatives = []
    else:
        representatives = reps
    
    for clust in clusters:
        n_samples = len(clust)
        linear_sum = np.sum(clust, axis=0)
        isim_clusts += jt_isim(linear_sum, n_samples)
        if not reps:
            if rep_type == 'centroid':
                representatives.append(calculate_centroid(linear_sum, n_samples))
            elif rep_type == 'medoid':
                medoid = calculate_medoid(clust)
                representatives.append(clust[medoid])
    
    av_isim_clusts = isim_clusts/n_clusters
    
    representatives = np.array(representatives)
    rep_linear_sum = np.sum(representatives, axis=0)
    rep_isim = jt_isim(rep_linear_sum, n_clusters)

    try:
        value =  rep_isim/av_isim_clusts
    except:
        value = 0
    
    return value