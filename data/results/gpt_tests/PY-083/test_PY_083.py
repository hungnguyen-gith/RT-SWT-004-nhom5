import pytest

class TestBindFunction:
    def setup_method(self):
        self.module = YourModuleClass()  # Replace with the actual class name
        self.module.binded = False
        self.module._data_names = ['data1', 'data2']
        self.module._label_names = ['label1']
        self.module._compute_output_shapes = lambda: [('output1', (1,)), ('output2', (1,))]

    def test_normal_case(self):
        data_shapes = [('data1', (1, 2)), ('data2', (1, 3))]
        label_shapes = [('label1', (1, 1))]
        self.module.bind(data_shapes, label_shapes)
        assert self.module._data_shapes == data_shapes
        assert self.module._label_shapes == label_shapes

    def test_no_label_shapes(self):
        data_shapes = [('data1', (1, 2)), ('data2', (1, 3))]
        self.module.bind(data_shapes)
        assert self.module._data_shapes == data_shapes
        assert self.module._label_shapes is None

    def test_force_rebind(self):
        self.module.binded = True
        data_shapes = [('data1', (1, 2)), ('data2', (1, 3))]
        self.module.bind(data_shapes, force_rebind=True)
        assert self.module._data_shapes == data_shapes

    def test_grad_req_write(self):
        data_shapes = [('data1', (1, 2)), ('data2', (1, 3))]
        self.module.bind(data_shapes, grad_req='write')
        assert self.module.for_training is True

    def test_grad_req_invalid(self):
        data_shapes = [('data1', (1, 2)), ('data2', (1, 3))]
        with pytest.raises(AssertionError):
            self.module.bind(data_shapes, grad_req='invalid')

    def test_data_shapes_length_mismatch(self):
        data_shapes = [('data1', (1, 2))]
        with pytest.raises(AssertionError):
            self.module.bind(data_shapes)

    def test_data_names_mismatch(self):
        data_shapes = [('data1', (1, 2)), ('data3', (1, 3))]
        with pytest.raises(AssertionError):
            self.module.bind(data_shapes)

    def test_label_shapes_length_mismatch(self):
        data_shapes = [('data1', (1, 2)), ('data2', (1, 3))]
        label_shapes = [('label1', (1, 1)), ('label2', (1, 1))]
        with pytest.raises(AssertionError):
            self.module.bind(data_shapes, label_shapes)

    def test_label_names_mismatch(self):
        data_shapes = [('data1', (1, 2)), ('data2', (1, 3))]
        label_shapes = [('label2', (1, 1))]
        with pytest.raises(AssertionError):
            self.module.bind(data_shapes, label_shapes)

    def test_empty_data_shapes(self):
        data_shapes = []
        with pytest.raises(AssertionError):
            self.module.bind(data_shapes)

    def test_empty_label_shapes(self):
        data_shapes = [('data1', (1, 2)), ('data2', (1, 3))]
        label_shapes = []
        self.module.bind(data_shapes, label_shapes)
        assert self.module._label_shapes == label_shapes