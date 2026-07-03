def get_plot_metrics(clusters, cai, fps, smiles, top=20):
    sort_clusters = sort_clusters = sorted(clusters, key=lambda x: len(x), reverse=True)
    biggest_clusters = sort_clusters[:top]
    fps_biggest_clusters = [[fps[i] for i in c] for c in biggest_clusters]

    n_mol_bcs = [len(x) for x in biggest_clusters] # #molecules


    n_scaff = [cai.scaffold_analysis(c)[0] for c in biggest_clusters]
    isim_scaff = [cai.scaffold_analysis(c)[1] for c in biggest_clusters]


    isim_clusters = [jt_isim(np.sum(fpsc, axis=0), n) for fpsc,n in zip(fps_biggest_clusters, n_mol_bcs)]

    return n_mol_bcs, n_scaff, isim_scaff, isim_clusters