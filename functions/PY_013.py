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