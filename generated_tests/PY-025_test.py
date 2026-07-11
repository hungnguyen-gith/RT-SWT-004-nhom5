import pytest

class MockLayer:
    def __init__(self):
        self.layer_norm = MockLayerNorm()
        self.o_net = MockWeight()
        self.qkv_net = MockWeight()
        self.r_net = MockWeight()
        self.pos_ff = MockPosFF()

class MockLayerNorm:
    def __init__(self):
        self.weight = "layer_norm_weight"
        self.bias = "layer_norm_bias"

class MockWeight:
    def __init__(self):
        self.weight = "weight_value"

class MockPosFF:
    def __init__(self):
        self.layer_norm = MockLayerNorm()
        self.CoreNet = [MockWeight(), MockWeight(), MockWeight(), MockWeight()]

class MockModel:
    def __init__(self):
        self.transformer = True
        self.crit = MockCrit()
        self.word_emb = MockWordEmb()
        self.layers = [MockLayer() for _ in range(2)]
        self.r_r_bias = "r_r_bias_value"
        self.r_w_bias = "r_w_bias_value"

class MockCrit:
    def __init__(self):
        self.cluster_weight = "cluster_weight_value"
        self.cluster_bias = "cluster_bias_value"
        self.out_layers = [MockWeight() for _ in range(2)]
        self.out_projs = [MockWeight() for _ in range(2)]

class MockWordEmb:
    def __init__(self):
        self.emb_layers = [MockWeight() for _ in range(2)]
        self.emb_projs = [MockWeight() for _ in range(2)]

class MockConfig:
    def __init__(self, tie_weight=True, tie_projs=[True, False], untie_r=False):
        self.tie_weight = tie_weight
        self.tie_projs = tie_projs
        self.untie_r = untie_r

def test_build_tf_to_pytorch_map_normal():
    model = MockModel()
    config = MockConfig()
    result = build_tf_to_pytorch_map(model, config)
    assert isinstance(result, dict)
    assert len(result) > 0
    assert result["transformer/adaptive_softmax/cutoff_0/cluster_W"] == "cluster_weight_value"
    assert result["transformer/adaptive_softmax/cutoff_0/cluster_b"] == "cluster_bias_value"

def test_build_tf_to_pytorch_map_boundary():
    model = MockModel()
    config = MockConfig(tie_projs=[True])
    result = build_tf_to_pytorch_map(model, config)
    assert "transformer/adaptive_softmax/cutoff_0/b" in result
    assert "transformer/adaptive_softmax/cutoff_1/b" not in result

def test_build_tf_to_pytorch_map_edge_case_no_layers():
    model = MockModel()
    model.layers = []
    config = MockConfig()
    result = build_tf_to_pytorch_map(model, config)
    assert "transformer/r_r_bias" in result
    assert result["transformer/r_r_bias"] == ["r_r_bias_value"]

def test_build_tf_to_pytorch_map_edge_case_untie_r():
    model = MockModel()
    config = MockConfig(untie_r=True)
    result = build_tf_to_pytorch_map(model, config)
    assert "transformer/r_r_bias" in result
    assert result["transformer/r_r_bias"] == ["r_r_bias_value", "r_r_bias_value"]

def test_build_tf_to_pytorch_map_not_implemented():
    model = MockModel()
    config = MockConfig(tie_weight=False)
    with pytest.raises(NotImplementedError):
        build_tf_to_pytorch_map(model, config)