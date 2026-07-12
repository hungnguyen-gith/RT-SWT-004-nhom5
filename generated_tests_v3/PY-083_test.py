from functions.PY_083 import bind
import pytest

class Stub:
    def __init__(self):
        self.binded = False
        self.logger = self.Logger()
        self._data_names = ['data1', 'data2']
        self._label_names = ['label1']
        self._data_shapes = None
        self._label_shapes = None

    class Logger:
        def warning(self, msg):
            pass

    def _compute_output_shapes(self):
        return [(name, (1,)) for name in self._data_names]

def test_bind_success():
    stub = Stub()
    data_shapes = [('data1', (1,)), ('data2', (1,))]
    label_shapes = [('label1', (1,))]
    
    bind(stub, data_shapes, label_shapes)
    
    assert stub._data_shapes == data_shapes
    assert stub._label_shapes == label_shapes
    assert stub.for_training is True
    assert stub.inputs_need_grad is False

def test_bind_force_rebind():
    stub = Stub()
    stub.binded = True
    data_shapes = [('data1', (1,)), ('data2', (1,))]
    
    bind(stub, data_shapes, force_rebind=True)
    
    assert stub._data_shapes == data_shapes

def test_bind_already_bound():
    stub = Stub()
    stub.binded = True
    data_shapes = [('data1', (1,)), ('data2', (1,))]
    
    bind(stub, data_shapes)
    
    assert stub._data_shapes is None

def test_bind_invalid_grad_req():
    stub = Stub()
    data_shapes = [('data1', (1,)), ('data2', (1,))]
    
    with pytest.raises(AssertionError, match="Python module only support write gradient"):
        bind(stub, data_shapes, grad_req='add')

def test_bind_shape_mismatch():
    stub = Stub()
    data_shapes = [('data1', (1,)), ('data2', (1,))]
    label_shapes = [('label1', (1,)), ('label2', (1,))]
    
    with pytest.raises(AssertionError):
        bind(stub, data_shapes, label_shapes)

def test_bind_label_shapes_none():
    stub = Stub()
    data_shapes = [('data1', (1,)), ('data2', (1,))]
    
    bind(stub, data_shapes, label_shapes=None)
    
    assert stub._label_shapes is None

def test_bind_data_shapes_length_mismatch():
    stub = Stub()
    data_shapes = [('data1', (1,))]
    
    with pytest.raises(AssertionError):
        bind(stub, data_shapes)