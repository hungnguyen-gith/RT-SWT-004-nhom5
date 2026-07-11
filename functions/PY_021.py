import plotly.graph_objects as go


def mol_relocation_plots(brc_1, brc_2, top_n = 2, title=None):
    
    clusters_1 = brc_1.get_cluster_mol_ids()
    clusters_2 = brc_2.get_cluster_mol_ids()

    list_1 = sorted(clusters_1, key=lambda x: len(x), reverse=True)[:top_n]
    list_2 = sorted(clusters_2, key=lambda x: len(x), reverse=True)[:top_n]

    # Map elements to clusters
    cluster_map_1 = {elem: f"Cluster 1-{i}" for i, cluster in enumerate(list_1) for elem in cluster}
    cluster_map_2 = {elem: f"Cluster 2-{i}" for i, cluster in enumerate(list_2) for elem in cluster}

    # Track flow of elements between clusters
    flows = {}
    for elem in cluster_map_1:
        source = cluster_map_1[elem]
        target = cluster_map_2.get(elem, "Other smaller cluster")
        flow_key = (source, target)
        flows[flow_key] = flows.get(flow_key, 0) + 1

    # Prepare data for Sankey diagram
    labels = list(set([src for src, _ in flows] + [tgt for _, tgt in flows]))
    source_indices = [labels.index(src) for src, _ in flows]
    target_indices = [labels.index(tgt) for _, tgt in flows]
    values = list(flows.values())

    # Create Sankey diagram
    fig = go.Figure(data=[go.Sankey(
        node=dict(
            pad=15,
            thickness=20,
            line=dict(color="black", width=0.5),
            label=labels
        ),
        link=dict(
            source=source_indices,
            target=target_indices,
            value=values
        )
    )])

    # Update layout
    fig.update_layout(
        title_text=title,
        font_size=10
    )
    fig.show()