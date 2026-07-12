from functions.PY_020 import tsne_plot
import pytest
import numpy as np

class StubBrc:
    def __init__(self, clusters):
        self.clusters = clusters

    def get_cluster_mol_ids(self):
        return self.clusters

def test_tsne_plot_normal_case():
    brc = StubBrc([[0, 1, 2], [3, 4], [5]])
    fps = np.random.rand(6, 10)  # 6 molecules with 10 features each
    tsne_plot(brc, fps, method='test', title='Test Title')

def test_tsne_plot_empty_clusters():
    brc = StubBrc([])
    fps = np.random.rand(0, 10)  # No molecules
    tsne_plot(brc, fps, method='test', title='Test Title')

def test_tsne_plot_single_cluster():
    brc = StubBrc([[0]])
    fps = np.random.rand(1, 10)  # 1 molecule with 10 features
    tsne_plot(brc, fps, method='test', title='Test Title')

def test_tsne_plot_large_clusters():
    brc = StubBrc([[0, 1, 2, 3, 4, 5, 6, 7, 8, 9, 10, 11, 12, 13, 14, 15, 16, 17, 18, 19]])
    fps = np.random.rand(20, 10)  # 20 molecules with 10 features each
    tsne_plot(brc, fps, method='test', title='Test Title')

def test_tsne_plot_invalid_fps_shape():
    brc = StubBrc([[0, 1], [2, 3]])
    fps = np.random.rand(4, 5)  # 4 molecules with 5 features each
    with pytest.raises(ValueError):
        tsne_plot(brc, fps, method='test', title='Test Title')

def test_tsne_plot_no_title():
    brc = StubBrc([[0, 1, 2], [3, 4]])
    fps = np.random.rand(5, 10)  # 5 molecules with 10 features each
    tsne_plot(brc, fps, method='test')

def test_tsne_plot_method_case():
    brc = StubBrc([[0, 1], [2, 3]])
    fps = np.random.rand(4, 10)  # 4 molecules with 10 features each
    tsne_plot(brc, fps, method='example_method', title='Example Title')