import pytest
import numpy as np

class TestTrainFunction:
    class MockBuffer:
        def __init__(self, returns, value_preds, active_masks):
            self.returns = returns
            self.value_preds = value_preds
            self.active_masks = active_masks

        def recurrent_generator(self, advantages, num_mini_batch, data_chunk_length):
            yield from [(np.array([1.0]), np.array([1.0]), np.array([1.0]), np.array([1.0]), np.array([1.0]), np.array([1.0]))]

        def naive_recurrent_generator(self, advantages, num_mini_batch):
            yield from [(np.array([1.0]), np.array([1.0]), np.array([1.0]), np.array([1.0]), np.array([1.0]), np.array([1.0]))]

        def feed_forward_generator(self, advantages, num_mini_batch):
            yield from [(np.array([1.0]), np.array([1.0]), np.array([1.0]), np.array([1.0]), np.array([1.0]), np.array([1.0]))]

    class MockModel:
        def __init__(self, use_popart, use_recurrent_policy, use_naive_recurrent, ppo_epoch, num_mini_batch, data_chunk_length):
            self._use_popart = use_popart
            self._use_recurrent_policy = use_recurrent_policy
            self._use_naive_recurrent = use_naive_recurrent
            self.ppo_epoch = ppo_epoch
            self.num_mini_batch = num_mini_batch
            self.data_chunk_length = data_chunk_length
            self.value_normalizer = self.MockValueNormalizer()

        class MockValueNormalizer:
            def denormalize(self, value_preds):
                return value_preds

        def ppo_update(self, sample, update_actor):
            return (np.array([0.1]), np.array([0.1]), np.array([0.1]), np.array([0.1]), 0.1, np.array([1.0]))

    def test_train_with_popart_and_recurrent_policy(self):
        buffer = self.MockBuffer(np.array([1.0, 2.0]), np.array([1.0, 1.5]), np.array([1.0, 1.0]))
        model = self.MockModel(use_popart=True, use_recurrent_policy=True, use_naive_recurrent=False, ppo_epoch=1, num_mini_batch=1, data_chunk_length=1)
        train_info = model.train(buffer)
        assert 'value_loss' in train_info
        assert 'policy_loss' in train_info
        assert 'dist_entropy' in train_info

    def test_train_without_popart_and_naive_recurrent(self):
        buffer = self.MockBuffer(np.array([1.0, 2.0]), np.array([1.0, 1.5]), np.array([1.0, 1.0]))
        model = self.MockModel(use_popart=False, use_recurrent_policy=False, use_naive_recurrent=True, ppo_epoch=1, num_mini_batch=1, data_chunk_length=1)
        train_info = model.train(buffer)
        assert 'value_loss' in train_info
        assert 'policy_loss' in train_info
        assert 'dist_entropy' in train_info

    def test_train_without_popart_and_feed_forward(self):
        buffer = self.MockBuffer(np.array([1.0, 2.0]), np.array([1.0, 1.5]), np.array([1.0, 1.0]))
        model = self.MockModel(use_popart=False, use_recurrent_policy=False, use_naive_recurrent=False, ppo_epoch=1, num_mini_batch=1, data_chunk_length=1)
        train_info = model.train(buffer)
        assert 'value_loss' in train_info
        assert 'policy_loss' in train_info
        assert 'dist_entropy' in train_info

    def test_train_with_zero_active_masks(self):
        buffer = self.MockBuffer(np.array([1.0, 2.0]), np.array([1.0, 1.5]), np.array([0.0, 0.0]))
        model = self.MockModel(use_popart=False, use_recurrent_policy=False, use_naive_recurrent=False, ppo_epoch=1, num_mini_batch=1, data_chunk_length=1)
        train_info = model.train(buffer)
        assert np.isnan(train_info['value_loss'])
        assert np.isnan(train_info['policy_loss'])
        assert np.isnan(train_info['dist_entropy'])