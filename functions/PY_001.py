def set_merge(merge_criterion, tolerance=0.05):
    """
    Sets merge_accept function for merge_subcluster, based on user specified merge_criteria. 

    Radius: merge subcluster based on comparison to centroid of the cluster
    Diameter: merge subcluster based on instant Tanimoto similarity of cluster
    Tolerance: applies tolerance threshold to diameter merge criteria, which will merge subcluster with stricter threshold for newly added molecules

    Parameters:
    -----------
    merge_criterion: str(); 
                        radius, diameter or tolerance
    tolerance: float; 
                        sets penalty value for similarity threshold when callng tolerance merge criteria

    Returns:
    --------
    merge_accept(): function 
                        if cluster is accepted to merge, merge the cluster based on the criteria specified
    """
    if merge_criterion == 'radius':
        def merge_accept(threshold, new_ls, new_centroid, new_n, old_ls, nom_ls, old_n, nom_n):
            jt_sim = jt_isim(new_ls + new_centroid, new_n + 1) * (new_n + 1) - jt_isim(new_ls, new_n) * (new_n - 1)
            return jt_sim >= threshold*2
    elif merge_criterion == 'diameter':
        def merge_accept(threshold, new_ls, new_centroid, new_n, old_ls, nom_ls, old_n, nom_n): 
            jt_radius = jt_isim(new_ls, new_n)
            return jt_radius >= threshold
    elif merge_criterion == 'tolerance_tough':
        def merge_accept(threshold, new_ls, new_centroid, new_n, old_ls, nom_ls, old_n, nom_n):
            jt_radius = jt_isim(new_ls, new_n)
            if jt_radius < threshold:
                return False
            else:
                if old_n == 1 and nom_n == 1:
                    return True
                elif nom_n == 1:
                    return (jt_isim(old_ls + nom_ls, old_n + 1) * (old_n + 1) - jt_isim(old_ls, old_n) * (old_n - 1))/2 >= jt_isim(old_ls, old_n) - tolerance and (jt_radius >= threshold)
                else:
                    return (jt_isim(old_ls + nom_ls, old_n + nom_n) * (old_n + nom_n) * (old_n + nom_n - 1) 
                    - jt_isim(old_ls, old_n) * old_n * (old_n - 1)
                    - jt_isim(nom_ls, nom_n) * nom_n * (nom_n - 1))/(2 * old_n * nom_n) >= jt_isim(old_ls, old_n) - tolerance and (jt_radius >= threshold)
    elif merge_criterion == 'tolerance':
        def merge_accept(threshold, new_ls, new_centroid, new_n, old_ls, nom_ls, old_n, nom_n):
            jt_radius = jt_isim(new_ls, new_n)
            if jt_radius < threshold:
                return False
            else:
                if old_n == 1 and nom_n == 1:
                    return True
                elif nom_n == 1:
                    return (jt_isim(old_ls + nom_ls, old_n + 1) * (old_n + 1) - jt_isim(old_ls, old_n) * (old_n - 1))/2 >= jt_isim(old_ls, old_n) - tolerance and (jt_radius >= threshold)
                else:
                    return True
    globals()['merge_accept'] = merge_accept