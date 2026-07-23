import pytest
import numpy as np

class TestUpdateFunction:
    @pytest.fixture
    def setup(self):
        class MockModel:
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
                self.visual_in = ['visual_in0', 'visual_in1']
                self.memory_in = 'memory_in'
                self.act_size = [2]
                self.vis_obs_size = 3

        class MockSelf:
            def __init__(self):
                self.model = MockModel()
                self.use_continuous_act = False
                self.use_recurrent = False
                self.use_vec_obs = False
                self.use_curiosity = False
                self.sequence_length = 1
                self.vec_obs_size = 4
                self.brain = MockModel()
                self.has_updated = False

            def _execute_model(self, feed_dict, update_dict):
                return "model_output"

        return MockSelf()

    def test_normal_case(self, setup):
        mini_batch = {
            'masks': np.array([[1, 1], [1, 1]]),
            'discounted_returns': np.array([[0.5], [0.5]]),
            'value_estimates': np.array([[0.1], [0.1]]),
            'advantages': np.array([[0.2], [0.2]]),
            'action_probs': np.array([[0.3, 0.4]]),
            'actions': np.array([[1, 0]]),
            'action_mask': np.array([[1, 1]]),
            'vector_obs': np.array([[0.1, 0.2, 0.3, 0.4]]),
            'prev_action': np.array([[0]]),
            'memory': np.array([[[0.5, 0.5]]]),
        }
        output = setup.update(mini_batch, 2)
        assert output == "model_output"
        assert setup.has_updated

    def test_boundary_case_empty_mini_batch(self, setup):
        mini_batch = {
            'masks': np.array([]),
            'discounted_returns': np.array([]),
            'value_estimates': np.array([]),
            'advantages': np.array([]),
            'action_probs': np.array([]),
            'actions': np.array([]),
            'action_mask': np.array([]),
            'vector_obs': np.array([]),
            'prev_action': np.array([]),
            'memory': np.array([]),
        }
        output = setup.update(mini_batch, 0)
        assert output == "model_output"
        assert setup.has_updated

    def test_edge_case_single_element(self, setup):
        mini_batch = {
            'masks': np.array([[1]]),
            'discounted_returns': np.array([[0.5]]),
            'value_estimates': np.array([[0.1]]),
            'advantages': np.array([[0.2]]),
            'action_probs': np.array([[0.3]]),
            'actions': np.array([[1]]),
            'action_mask': np.array([[1]]),
            'vector_obs': np.array([[0.1, 0.2, 0.3, 0.4]]),
            'prev_action': np.array([[0]]),
            'memory': np.array([[[0.5]]]),
        }
        output = setup.update(mini_batch, 1)
        assert output == "model_output"
        assert setup.has_updated

    def test_edge_case_large_inputs(self, setup):
        mini_batch = {
            'masks': np.ones((1000, 1000)),
            'discounted_returns': np.ones((1000, 1)),
            'value_estimates': np.ones((1000, 1)),
            'advantages': np.ones((1000, 1)),
            'action_probs': np.ones((1000, 2)),
            'actions': np.ones((1000, 2)),
            'action_mask': np.ones((1000, 2)),
            'vector_obs': np.ones((1000, 4)),
            'prev_action': np.ones((1000, 1)),
            'memory': np.ones((1000, 1, 2)),
        }
        output = setup.update(mini_batch, 1000)
        assert output == "model_output"
        assert setup.has_updated