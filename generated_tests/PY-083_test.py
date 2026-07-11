import pytest

class TestBindFunction:
    def setup_method(self):
        self.module = YourModuleClass()  # Replace with the actual class name
        self.module._data_names = ['data1', 'data2']
        self.module._label_names = ['label1']
        self.module.binded = False

    def test_normal_case(self):
        data_shapes = [('data1', (3, 224, 224)), ('data2', (3, 224, 224))]
        label_shapes = [('label1', (1,))]
        self.module.bind(data_shapes, label_shapes)
        assert self.module._data_shapes == data_shapes
        assert self.module._label_shapes == label_shapes

    def test_no_label_shapes(self):
        data_shapes = [('data1', (3, 224, 224)), ('data2', (3, 224, 224))]
        self.module.bind(data_shapes)
        assert self.module._data_shapes == data_shapes
        assert self.module._label_shapes is None

    def test_force_rebind(self):
        self.module.binded = True
        data_shapes = [('data1', (3, 224, 224)), ('data2', (3, 224, 224))]
        self.module.bind(data_shapes, force_rebind=True)
        assert self.module._data_shapes == data_shapes

    def test_grad_req_write(self):
        data_shapes = [('data1', (3, 224, 224)), ('data2', (3, 224, 224))]
        self.module.bind(data_shapes, grad_req='write')
        assert self.module.for_training is True

    def test_grad_req_invalid(self):
        data_shapes = [('data1', (3, 224, 224)), ('data2', (3, 224, 224))]
        with pytest.raises(AssertionError, match="Python module only support write gradient"):
            self.module.bind(data_shapes, grad_req='add')

    def test_boundary_case_empty_data_shapes(self):
        data_shapes = []
        label_shapes = []
        self.module.bind(data_shapes, label_shapes)
        assert self.module._data_shapes == data_shapes
        assert self.module._label_shapes == label_shapes

    def test_boundary_case_single_data_shape(self):
        data_shapes = [('data1', (3, 224, 224))]
        label_shapes = [('label1', (1,))]
        self.module.bind(data_shapes, label_shapes)
        assert self.module._data_shapes == data_shapes
        assert self.module._label_shapes == label_shapes

    def test_edge_case_mismatched_data_names(self):
        data_shapes = [('data1', (3, 224, 224)), ('data3', (3, 224, 224))]
        with pytest.raises(AssertionError):
            self.module.bind(data_shapes)

    def test_edge_case_mismatched_label_names(self):
        data_shapes = [('data1', (3, 224, 224)), ('data2', (3, 224, 224))]
        label_shapes = [('label2', (1,))]
        with pytest.raises(AssertionError):
            self.module.bind(data_shapes, label_shapes)