from functions.PY_028 import tie_weights

class Stub:
    def __init__(self, sample_softmax, tie_weight, tie_projs, div_val, d_model, d_embed, out_layers, out_projs, word_emb):
        self.sample_softmax = sample_softmax
        self.config = Config(tie_weight, tie_projs, div_val, d_model, d_embed)
        self.crit = Crit(out_layers, out_projs)
        self.transformer = Transformer(word_emb)
        self.out_layer = out_layers[0] if out_layers else None

class Config:
    def __init__(self, tie_weight, tie_projs, div_val, d_model, d_embed):
        self.tie_weight = tie_weight
        self.tie_projs = tie_projs
        self.div_val = div_val
        self.d_model = d_model
        self.d_embed = d_embed

class Crit:
    def __init__(self, out_layers, out_projs):
        self.out_layers = out_layers
        self.out_projs = out_projs

class Transformer:
    def __init__(self, word_emb):
        self.word_emb = word_emb

class WordEmb:
    def __init__(self, weight, emb_layers, emb_projs):
        self.weight = weight
        self.emb_layers = emb_layers
        self.emb_projs = emb_projs

def test_tie_weights_sampled_softmax():
    word_emb = WordEmb(weight='word_weight', emb_layers=[], emb_projs=[])
    stub = Stub(sample_softmax=1, tie_weight=True, tie_projs=[], div_val=1, d_model=512, d_embed=256, out_layers=[word_emb], out_projs=[], word_emb=word_emb)
    tie_weights(stub)
    assert stub.out_layer.weight == 'word_weight'

def test_tie_weights_adaptive_softmax():
    emb_layer1 = WordEmb(weight='layer1_weight', emb_layers=[], emb_projs=[])
    emb_layer2 = WordEmb(weight='layer2_weight', emb_layers=[], emb_projs=[])
    word_emb = WordEmb(weight=None, emb_layers=[emb_layer1, emb_layer2], emb_projs=[])
    stub = Stub(sample_softmax=0, tie_weight=True, tie_projs=[], div_val=1, d_model=512, d_embed=256, out_layers=[emb_layer1, emb_layer2], out_projs=[None, None], word_emb=word_emb)
    tie_weights(stub)
    assert stub.crit.out_layers[0].weight == 'layer1_weight'
    assert stub.crit.out_layers[1].weight == 'layer2_weight'

def test_tie_weights_with_projs():
    emb_layer = WordEmb(weight='layer_weight', emb_layers=[], emb_projs=['proj1', 'proj2'])
    word_emb = WordEmb(weight=None, emb_layers=[emb_layer], emb_projs=['proj1', 'proj2'])
    stub = Stub(sample_softmax=0, tie_weight=True, tie_projs=[True, True], div_val=1, d_model=512, d_embed=256, out_layers=[emb_layer], out_projs=[None, None], word_emb=word_emb)
    tie_weights(stub)
    assert stub.crit.out_projs[0] == 'proj1'

def test_tie_weights_invalid_div_val():
    emb_layer = WordEmb(weight='layer_weight', emb_layers=[], emb_projs=['proj1', 'proj2'])
    word_emb = WordEmb(weight=None, emb_layers=[emb_layer], emb_projs=['proj1', 'proj2'])
    stub = Stub(sample_softmax=0, tie_weight=True, tie_projs=[True, True], div_val=2, d_model=512, d_embed=256, out_layers=[emb_layer], out_projs=[None, None], word_emb=word_emb)
    tie_weights(stub)
    assert stub.crit.out_projs[0] == 'proj1'  # Should still tie to proj1

def test_tie_weights_no_tie_weight():
    word_emb = WordEmb(weight='word_weight', emb_layers=[], emb_projs=[])
    stub = Stub(sample_softmax=1, tie_weight=False, tie_projs=[], div_val=1, d_model=512, d_embed=256, out_layers=[word_emb], out_projs=[], word_emb=word_emb)
    tie_weights(stub)
    assert stub.out_layer.weight == 'word_weight'  # Should still be 'word_weight'

def test_tie_weights_no_tie_projs():
    emb_layer = WordEmb(weight='layer_weight', emb_layers=[], emb_projs=['proj1', 'proj2'])
    word_emb = WordEmb(weight=None, emb_layers=[emb_layer], emb_projs=['proj1', 'proj2'])
    stub = Stub(sample_softmax=0, tie_weight=True, tie_projs=[False, False], div_val=1, d_model=512, d_embed=256, out_layers=[emb_layer], out_projs=[None, None], word_emb=word_emb)
    tie_weights(stub)
    assert stub.crit.out_projs[0] != 'proj1'  # Should not tie to proj1