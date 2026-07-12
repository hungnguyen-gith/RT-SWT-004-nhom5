from functions.PY_037 import update
import pytest
import numpy as np

class StubModel:
    def __init__(self):
        self.batch_size = 'batch_size'
        self.sequence_length = 'sequence_length'
        self.mask_input = 'mask_input'
        self.returns_holder = 'returns_holder'
        self.old_value = 'old_value'
        self.advantage = 'advantage'
        self.all_old_log_probs = 'all_old_log_probs'
        self.output_pre = 'output_pre'
        self.epsilon = 'epsilon'
        self.action_holder = 'action_holder'
        self.prev_action = 'prev_action'
        self.action_masks = 'action_masks'
        self.vector_in = 'vector_in'
        self.visual_in = ['visual_in_0', 'visual_in_1']
        self.next_vector_in = 'next_vector_in'
        self.next_visual_in = ['next_visual_in_0', 'next_visual_in_1']
        self.memory_in = 'memory_in'
        self.act_size = [2]
        self.vis_obs_size = 2

class Stub:
    def __init__(self):
        self.model = StubModel()
        self.use_continuous_act = False
        self.use_recurrent = False
        self.use_vec_obs = False
        self.use_curiosity = False
        self.sequence_length = 1
        self.brain = StubBrain()
        self.vec_obs_size = 2
        self.has_updated = False
        self.update_dict = {}

    def _execute_model(self, feed_dict, update_dict):
        return "model_output"

class StubBrain:
    def __init__(self):
        self.vector_action_space_size = [2]

def test_update_normal_case():
    stub = Stub()
    mini_batch = {
        'masks': np.array([[1], [1]]),
        'discounted_returns': np.array([[1], [1]]),
        'value_estimates': np.array([[1], [1]]),
        'advantages': np.array([[1], [1]]),
        'action_probs': np.array([[1], [1]]),
        'actions': np.array([[1], [1]]),
        'action_mask': np.array([[1], [1]]),
        'vector_obs': np.array([[1, 1], [1, 1]]),
        'visual_obs0': np.array([[1, 1, 1], [1, 1, 1]]),
        'visual_obs1': np.array([[1, 1, 1], [1, 1, 1]]),
        'memory': np.array([[[1, 1], [1, 1]]])
    }
    output = update(stub, mini_batch, num_sequences=2)
    assert output == "model_output"
    assert stub.has_updated is True

def test_update_with_recurrent():
    stub = Stub()
    stub.use_recurrent = True
    mini_batch = {
        'masks': np.array([[1], [1]]),
        'discounted_returns': np.array([[1], [1]]),
        'value_estimates': np.array([[1], [1]]),
        'advantages': np.array([[1], [1]]),
        'action_probs': np.array([[1], [1]]),
        'actions': np.array([[1], [1]]),
        'prev_action': np.array([[1], [1]]),
        'action_mask': np.array([[1], [1]]),
        'vector_obs': np.array([[1, 1], [1, 1]]),
        'visual_obs0': np.array([[1, 1, 1], [1, 1, 1]]),
        'visual_obs1': np.array([[1, 1, 1], [1, 1, 1]]),
        'memory': np.array([[[1, 1], [1, 1]]])
    }
    output = update(stub, mini_batch, num_sequences=2)
    assert output == "model_output"
    assert stub.has_updated is True

def test_update_with_vector_obs():
    stub = Stub()
    stub.use_vec_obs = True
    mini_batch = {
        'masks': np.array([[1], [1]]),
        'discounted_returns': np.array([[1], [1]]),
        'value_estimates': np.array([[1], [1]]),
        'advantages': np.array([[1], [1]]),
        'action_probs': np.array([[1], [1]]),
        'actions': np.array([[1], [1]]),
        'action_mask': np.array([[1], [1]]),
        'vector_obs': np.array([[1, 1], [1, 1]]),
        'visual_obs0': np.array([[1, 1, 1], [1, 1, 1]]),
        'visual_obs1': np.array([[1, 1, 1], [1, 1, 1]]),
        'memory': np.array([[[1, 1], [1, 1]]])
    }
    output = update(stub, mini_batch, num_sequences=2)
    assert output == "model_output"
    assert stub.has_updated is True

def test_update_with_invalid_input():
    stub = Stub()
    mini_batch = {
        'masks': np.array([[None], [None]]),
        'discounted_returns': np.array([[None], [None]]),
        'value_estimates': np.array([[None], [None]]),
        'advantages': np.array([[None], [None]]),
        'action_probs': np.array([[None], [None]]),
        'actions': np.array([[None], [None]]),
        'prev_action': np.array([[None], [None]]),
        'action_mask': np.array([[None], [None]]),
        'vector_obs': np.array([[None, None], [None, None]]),
        'visual_obs0': np.array([[None, None, None], [None, None, None]]),
        'visual_obs1': np.array([[None, None, None], [None, None, None]]),
        'memory': np.array([[[None, None], [None, None]]])
    }
    with pytest.raises(TypeError):
        update(stub, mini_batch, num_sequences=2)