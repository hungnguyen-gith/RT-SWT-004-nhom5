def forward(self):
        print('Running Cluster Analysis: \n')
        print('Computing clustering metrics...')
        self.chi_val, self.dbi_val, self.dunn_val = self.clustering_metrics()
        print(f'Chi:{self.chi_val}')
        print(f'DBI:{self.dbi_val}')
        print(f'Dunn:{self.dunn_val}\n')

        print('Analyzing the biggest cluster...')
        biggest_cluster, fps_biggest_cluster = self.get_biggest_cluster()
        (self.n_biggest_cluster, self.isim_biggest_cluster, 
        self.isim_outliers, self.isim_medoids, self.radius_value) = self.biggest_cluster_metrics(biggest_cluster, fps_biggest_cluster)
        print(f'Size of biggest cluster: {self.n_biggest_cluster}')
        print(f'iSIM: {self.isim_biggest_cluster}')
        print(f'iSIM of the outliers: {self.isim_outliers}')
        print(f'iSIM of the medoids: {self.isim_medoids}')
        print(f'Radius of biggest_cluster: {self.radius_value} \n')

        print('Looking for unique scaffolds...')
        self.unique_scaffolds, self.scaffolds_iSIM = self.scaffold_analysis(biggest_cluster)
        print(f'Number of unique scaffolds: {self.unique_scaffolds}')
        print(f'iSIM of unique scaffolds: {self.scaffolds_iSIM} \n')
        
        print('Getting total clusters...')
        clusters = self.get_clusters()
        self.total_clusters = len(clusters)
        self.larger_clusters = [x for x in [len(cluster) > 10 for cluster in clusters] if x]
        print(f'Total number of clusters: {self.total_clusters}')
        print(f'Total number of clusters with more than 10 molecules: {len(self.larger_clusters)} \n')
        
        print('Analysis Complete!')
        
        return clusters