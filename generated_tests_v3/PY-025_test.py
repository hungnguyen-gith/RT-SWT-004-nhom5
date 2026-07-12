from functions.PY_025 import build_tf_to_pytorch_map
import pytest

class StubModel:
    def __init__(self):
        self.transformer = None
        self.crit = StubCrit()
        self.r_r_bias = "r_r_bias_tensor"
        self.r_w_bias = "r_w_bias_tensor"

class StubCrit:
    def __init__(self):
        self.cluster_weight = "cluster_weight_tensor"
        self.cluster_bias = "cluster_bias_tensor"
        self.out_layers = [StubLayer(), StubLayer()]
        self.out_projs = ["out_proj_1", "out_proj_2"]

class StubLayer:
    def __init__(self):
        self.bias = "layer_bias_tensor"
        self.weight = "layer_weight_tensor"

class StubConfig:
    def __init__(self, tie_weight=True, tie_projs=[True, False], untie_r=False):
        self.tie_weight = tie_weight
        self.tie_projs = tie_projs
        self.untie_r = untie_r

class StubTransformer:
    def __init__(self):
        self.word_emb = StubWordEmb()
        self.layers = [StubBlock(), StubBlock()]

class StubWordEmb:
    def __init__(self):
        self.emb_layers = [StubEmbedLayer(), StubEmbedLayer()]
        self.emb_projs = ["embed_proj_1", "embed_proj_2"]

class StubEmbedLayer:
    def __init__(self):
        self.weight = "embed_weight_tensor"

class StubBlock:
    def __init__(self):
        self.dec_attn = StubDecAttn()
        self.pos_ff = StubPosFF()

class StubDecAttn:
    def __init__(self):
        self.layer_norm = StubLayerNorm()
        self.o_net = StubWeight()
        self.qkv_net = StubWeight()
        self.r_net = StubWeight()
        self.r_r_bias = "r_r_bias_tensor"
        self.r_w_bias = "r_w_bias_tensor"

class StubPosFF:
    def __init__(self):
        self.layer_norm = StubLayerNorm()
        self.CoreNet = [StubWeight(), StubWeight(), StubWeight(), StubWeight()]

class StubLayerNorm:
    def __init__(self):
        self.weight = "layer_norm_weight"
        self.bias = "layer_norm_bias"

class StubWeight:
    def __init__(self):
        self.weight = "weight_tensor"
        self.bias = "bias_tensor"

def test_build_tf_to_pytorch_map_with_transformer():
    model = StubModel()
    model.transformer = StubTransformer()
    config = StubConfig()
    
    result = build_tf_to_pytorch_map(model, config)
    
    assert result["transformer/adaptive_softmax/cutoff_0/cluster_W"] == "cluster_weight_tensor"
    assert result["transformer/adaptive_softmax/cutoff_0/cluster_b"] == "cluster_bias_tensor"
    assert result["transformer/adaptive_softmax/cutoff_0/b"] == "layer_bias_tensor"
    assert result["transformer/adaptive_softmax/cutoff_1/b"] == "layer_bias_tensor"
    assert result["transformer/adaptive_embed/cutoff_0/lookup_table"] == "embed_weight_tensor"
    assert result["transformer/adaptive_embed/cutoff_0/proj_W"] == "embed_proj_1"
    assert result["transformer/layer_0/rel_attn/LayerNorm/gamma"] == "layer_norm_weight"
    assert result["transformer/layer_0/rel_attn/o/kernel"] == "weight_tensor"
    assert result["transformer/layer_0/ff/layer_1/kernel"] == "weight_tensor"
    assert result["transformer/r_r_bias"] == ["r_r_bias_tensor", "r_r_bias_tensor"]
    assert result["transformer/r_w_bias"] == ["r_w_bias_tensor", "r_w_bias_tensor"]

def test_build_tf_to_pytorch_map_with_untie_r():
    model = StubModel()
    model.transformer = StubTransformer()
    config = StubConfig(untie_r=True)
    
    result = build_tf_to_pytorch_map(model, config)
    
    assert result["transformer/r_r_bias"] == ["r_r_bias_tensor", "r_r_bias_tensor"]
    assert result["transformer/r_w_bias"] == ["r_w_bias_tensor", "r_w_bias_tensor"]

def test_build_tf_to_pytorch_map_with_not_tied_weights():
    model = StubModel()
    model.transformer = StubTransformer()
    config = StubConfig(tie_weight=False)
    
    with pytest.raises(NotImplementedError):
        build_tf_to_pytorch_map(model, config)

def test_build_tf_to_pytorch_map_without_transformer():
    model = StubModel()
    model.transformer = None
    config = StubConfig()
    
    result = build_tf_to_pytorch_map(model, config)
    
    assert result == {}  # Expecting an empty map if no transformer is present.