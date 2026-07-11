import numpy as np
import matplotlib
matplotlib.use('Agg')
import matplotlib.pyplot as plt
from sklearn.preprocessing import StandardScaler
from sklearn.manifold import TSNE


def tsne_plot(brc, fps, method='', title=None):
    clusters = brc.get_cluster_mol_ids()
    sort_clusters = sorted(clusters, key=lambda x: len(x), reverse=True)[:20]
    # #     # Map each mol ID to its cluster ID
    n_molecules = sum([len(x) for x in sort_clusters])


    cluster_labels = [0] * n_molecules

    fps_clusters = []#[0] * n_molecules
    cluster_labels = []#[0] * n_molecules

    for cluster_id, cluster in enumerate(sort_clusters):
        for idx in cluster:
            fps_clusters.append(fps[idx])
            cluster_labels.append(int(cluster_id))


    scaler = StandardScaler()
    fps_scaled = scaler.fit_transform(fps_clusters)

    tsne = TSNE(n_components=2, perplexity=30, random_state=42)
    fps_tsne = tsne.fit_transform(fps_scaled)

    plt.figure(figsize=(8, 6))
    scatter = plt.scatter(fps_tsne[:, 0], fps_tsne[:, 1], c=cluster_labels, cmap='tab20', alpha=0.9)
    cbar = plt.colorbar(scatter, label="Cluster ID")
    cbar.set_ticks(np.arange(20))  # Set ticks at the center of each color
    cbar.set_ticklabels(np.arange(1, 21))  # Set labels from 1 to 20
    plt.xlabel("t-SNE Component 1")
    plt.ylabel("t-SNE Component 2")
    if title:
        plt.title(f"t-SNE of Top 20 Largest Clusters for {title}")
    else:
        plt.title(f"t-SNE of Top 20 Largest Clusters for {method[0].upper() + method[1:]}")
    plt.show()