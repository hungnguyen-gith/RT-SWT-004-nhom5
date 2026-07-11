import pytest
import numpy as np
from unittest.mock import MagicMock

class TestTrainFunction:
    @pytest.fixture
    def setup(self):
        class MockBuffer:
            def __init__(self):
                self.returns = np.array([1.0, 2.0, 3.0])
                self.value_preds = np.array([1.0, 1.5, 2.5])
                self.active_masks = np.array([1.0, 1.0, 0.0])
                self.num_mini_batch = 2
                self.ppo_epoch = 1
                self.data_chunk_length = 1

            def recurrent_generator(self, advantages, num_mini_batch, data_chunk_length):
                yield (np.array([1.0]), np.array([1.0]), np.array([1.0]), np.array([1.0]), np.array([1.0]), np.array([1.0]))

            def feed_forward_generator(self, advantages, num_mini_batch):
                yield (np.array([1.0]), np.array([1.0]), np.array([1.0]), np.array([1.0]), np.array([1.0]), np.array([1.0]))

        class MockModel:
            def __init__(self):
                self._use_popart = False
                self._use_recurrent_policy = False
                self._use_naive_recurrent = False
                self.ppo_epoch = 1
                self.num_mini_batch = 1
                self.data_chunk_length = 1

            def ppo_update(self, sample, update_actor=True):
                return (1.0, 1.0, 1.0, 1.0, 1.0, np.array([1.0]))

        return MockModel(), MockBuffer()

    def test_train_normal_case(self, setup):
        model, buffer = setup
        train_info = model.train(buffer)
        assert isinstance(train_info, dict)
        assert train_info['value_loss'] == 1.0
        assert train_info['policy_loss'] == 1.0
        assert train_info['dist_entropy'] == 1.0
        assert train_info['actor_grad_norm'] == 1.0
        assert train_info['critic_grad_norm'] == 1.0
        assert train_info['ratio'] == 1.0

    def test_train_with_popart(self, setup):
        model, buffer = setup
        model._use_popart = True
        train_info = model.train(buffer)
        assert isinstance(train_info, dict)

    def test_train_with_zero_advantages(self, setup):
        model, buffer = setup
        buffer.returns = np.array([0.0, 0.0, 0.0])
        buffer.value_preds = np.array([0.0, 0.0, 0.0])
        train_info = model.train(buffer)
        assert isinstance(train_info, dict)

    def test_train_with_empty_buffer(self, setup):
        model, buffer = setup
        buffer.returns = np.array([])
        buffer.value_preds = np.array([])
        buffer.active_masks = np.array([])
        with pytest.raises(ValueError):
            model.train(buffer)

    def test_train_with_single_element_buffer(self, setup):
        model, buffer = setup
        buffer.returns = np.array([1.0])
        buffer.value_preds = np.array([1.0])
        buffer.active_masks = np.array([1.0])
        train_info = model.train(buffer)
        assert isinstance(train_info, dict)

    def test_train_with_nan_in_advantages(self, setup):
        model, buffer = setup
        buffer.returns = np.array([1.0, 2.0, 3.0])
        buffer.value_preds = np.array([1.0, 1.0, 1.0])
        buffer.active_masks = np.array([1.0, 1.0, 0.0])
        train_info = model.train(buffer)
        assert isinstance(train_info, dict)
        assert not np.isnan(train_info['value_loss'])