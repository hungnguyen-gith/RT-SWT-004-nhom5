import numpy as np
import pytest

class TestActFunction:
    class MockActor:
        def get_actions(self, cent_obs, obs, rnn_states_actor, rnn_states_critic, masks, available_actions, deterministic):
            return (None, np.array([1, 0]), None, rnn_states_actor, None)

    @pytest.fixture
    def setup_actor(self):
        return self.MockActor()

    def test_act_deterministic_with_available_actions(self, setup_actor):
        cent_obs = np.array([0.1, 0.2])
        obs = np.array([0.3, 0.4])
        rnn_states_actor = np.array([0.5, 0.6])
        masks = np.array([1, 0])
        available_actions = np.array([0, 1])
        deterministic = True
        
        actions, rnn_states_actor = setup_actor.act(cent_obs, obs, rnn_states_actor, masks, available_actions, deterministic)
        
        assert np.array_equal(actions, np.array([1, 0]))
        assert np.array_equal(rnn_states_actor, rnn_states_actor)

    def test_act_deterministic_without_available_actions(self, setup_actor):
        cent_obs = np.array([0.1, 0.2])
        obs = np.array([0.3, 0.4])
        rnn_states_actor = np.array([0.5, 0.6])
        masks = np.array([1, 0])
        available_actions = None
        deterministic = True
        
        actions, rnn_states_actor = setup_actor.act(cent_obs, obs, rnn_states_actor, masks, available_actions, deterministic)
        
        assert np.array_equal(actions, np.array([1, 0]))
        assert np.array_equal(rnn_states_actor, rnn_states_actor)

    def test_act_stochastic_with_available_actions(self, setup_actor):
        cent_obs = np.array([0.1, 0.2])
        obs = np.array([0.3, 0.4])
        rnn_states_actor = np.array([0.5, 0.6])
        masks = np.array([1, 0])
        available_actions = np.array([0, 1])
        deterministic = False
        
        actions, rnn_states_actor = setup_actor.act(cent_obs, obs, rnn_states_actor, masks, available_actions, deterministic)
        
        assert np.array_equal(actions, np.array([1, 0]))
        assert np.array_equal(rnn_states_actor, rnn_states_actor)

    def test_act_stochastic_without_available_actions(self, setup_actor):
        cent_obs = np.array([0.1, 0.2])
        obs = np.array([0.3, 0.4])
        rnn_states_actor = np.array([0.5, 0.6])
        masks = np.array([1, 0])
        available_actions = None
        deterministic = False
        
        actions, rnn_states_actor = setup_actor.act(cent_obs, obs, rnn_states_actor, masks, available_actions, deterministic)
        
        assert np.array_equal(actions, np.array([1, 0]))
        assert np.array_equal(rnn_states_actor, rnn_states_actor)

    def test_act_with_zero_masks(self, setup_actor):
        cent_obs = np.array([0.1, 0.2])
        obs = np.array([0.3, 0.4])
        rnn_states_actor = np.array([0.5, 0.6])
        masks = np.array([0, 0])
        available_actions = None
        deterministic = True
        
        actions, rnn_states_actor = setup_actor.act(cent_obs, obs, rnn_states_actor, masks, available_actions, deterministic)
        
        assert np.array_equal(actions, np.array([1, 0]))
        assert np.array_equal(rnn_states_actor, rnn_states_actor)