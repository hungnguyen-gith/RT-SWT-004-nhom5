def init_plot(method, title=None):
    csv_file = f"data/{method}_cluster_metrics.csv"

    if not os.path.exists(csv_file):
        print(f"Error: CSV file not found at {csv_file}")
    else:
        # Read CSV
        df = pd.read_csv(csv_file)

        # Ensure Cluster is treated as a categorical variable
        df["Cluster"] = df["Cluster"].astype(str)

        # Create figure and axes
        plt.figure(figsize=(10, 5))

        # Plot the number of molecules
        plt.bar(df["Cluster"], df["Number of Molecules"], color="blue", alpha=1, label="Molecules")
        
        # Annotate the number of molecules
        for i, mol in enumerate(df["Number of Molecules"]):
            plt.text(i, mol, f"{mol}", ha="center", va="bottom", fontsize=10, color="black")

        # Plot the number of unique scaffolds
        plt.bar(df["Cluster"], df["Number of Unique Scaffolds"], color="orange", alpha=1, label="Scaffolds")

        # Annotate the number of unique scaffolds
        for i, scaf in enumerate(df["Number of Unique Scaffolds"]):
            plt.text(i, scaf, f"{scaf}", ha="center", va="bottom", fontsize=8, color="white")

        # Labels
        plt.xlabel("Cluster", fontsize=12)
        plt.ylabel("Count", fontsize=12)
        plt.xticks(range(len(df["Cluster"])))
        plt.legend(loc="upper right")
     
     
        # Plot iSIM
        plt.twinx()
        plt.plot(df["Cluster"], df["iSIM"], color="green", marker="o", label="iSIM", linewidth=2)
        plt.ylabel("iSIM", fontsize=12)
        plt.yticks(np.arange(0, 1.1, 0.1))
        plt.ylim(0, 1)

        plt.tight_layout()

        plt.legend(loc="upper right", bbox_to_anchor=(0.80, 1))

        # Title
        if title:
            plt.title(f'Top 20 Cluster Metrics for {title}', fontsize=14)
        else:
            plt.title(f'Top 20 Cluster Metrics for {method[0].upper() + method[1:]}', fontsize=14)


        plt.show()