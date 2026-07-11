import pytest
from unittest.mock import MagicMock

class TestTieWeights:
    def setup_method(self):
        self.obj = MagicMock()
        self.obj.config.tie_weight = True
        self.obj.config.tie_projs = [True, False]
        self.obj.config.div_val = 1
        self.obj.config.d_model = 512
        self.obj.config.d_embed = 256
        self.obj.sample_softmax = 1
        self.obj.transformer.word_emb.weight = MagicMock()
        self.obj.crit.out_layers = [MagicMock(), MagicMock()]
        self.obj.crit.out_projs = [MagicMock(), MagicMock()]

    def test_tie_weights_sampled_softmax(self):
        self.obj.tie_weights()
        assert self.obj.out_layer.weight == self.obj.transformer.word_emb.weight

    def test_tie_weights_adaptive_softmax(self):
        self.obj.sample_softmax = 0
        self.obj.tie_weights()
        for i in range(len(self.obj.crit.out_layers)):
            assert self.obj.crit.out_layers[i].weight == self.obj.transformer.word_emb.emb_layers[i].weight

    def test_tie_projs_div_val_one(self):
        self.obj.sample_softmax = 0
        self.obj.tie_weights()
        for i, tie_proj in enumerate(self.obj.config.tie_projs):
            if tie_proj:
                assert self.obj.crit.out_projs[i] == self.obj.transformer.word_emb.emb_projs[0]

    def test_tie_projs_div_val_not_one(self):
        self.obj.config.div_val = 2
        self.obj.sample_softmax = 0
        self.obj.tie_weights()
        for i, tie_proj in enumerate(self.obj.config.tie_projs):
            if tie_proj:
                assert self.obj.crit.out_projs[i] == self.obj.transformer.word_emb.emb_projs[i]

    def test_no_tie_weight(self):
        self.obj.config.tie_weight = False
        self.obj.tie_weights()
        assert self.obj.out_layer.weight != self.obj.transformer.word_emb.weight

    def test_no_tie_projs(self):
        self.obj.config.tie_projs = [False, False]
        self.obj.tie_weights()
        assert self.obj.crit.out_projs == [MagicMock(), MagicMock()]

    def test_edge_case_empty_layers(self):
        self.obj.crit.out_layers = []
        self.obj.tie_weights()
        assert self.obj.crit.out_layers == []

    def test_edge_case_empty_projs(self):
        self.obj.crit.out_projs = []
        self.obj.tie_weights()
        assert self.obj.crit.out_projs == []