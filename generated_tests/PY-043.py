import pytest
import numpy as np
import torch

class TestGetActions:
    class MockModel:
        def actor(self, obs, rnn_states_actor, masks, available_actions, deterministic):
            actions = torch.tensor([1, 2, 3])
            action_log_probs = torch.tensor([0.1, 0.2, 0.3])
            rnn_states_actor = torch.tensor([0.5, 0.5])
            return actions, action_log_probs, rnn_states_actor

        def critic(self, cent_obs, rnn_states_critic, masks):
            values = torch.tensor([0.9])
            rnn_states_critic = torch.tensor([0.4])
            return values, rnn_states_critic

    def setup_method(self):
        self.model = self.MockModel()
        self.cent_obs = np.array([[0.1, 0.2]])
        self.obs = np.array([[0.3, 0.4]])
        self.rnn_states_actor = np.array([[0.5, 0.6]])
        self.rnn_states_critic = np.array([[0.7, 0.8]])
        self.masks = np.array([[1]])
    
    def test_get_actions_all_available(self):
        values, actions, action_log_probs, rnn_states_actor, rnn_states_critic = self.model.get_actions(
            self.cent_obs, self.obs, self.rnn_states_actor, self.rnn_states_critic, self.masks
        )
        assert values.shape == (1,)
        assert actions.shape == (3,)
        assert action_log_probs.shape == (3,)
        assert rnn_states_actor.shape == (2,)
        assert rnn_states_critic.shape == (1,)

    def test_get_actions_with_available_actions(self):
        available_actions = np.array([1, 0, 1])
        values, actions, action_log_probs, rnn_states_actor, rnn_states_critic = self.model.get_actions(
            self.cent_obs, self.obs, self.rnn_states_actor, self.rnn_states_critic, self.masks, available_actions
        )
        assert values.shape == (1,)
        assert actions.shape == (3,)
        assert action_log_probs.shape == (3,)
        assert rnn_states_actor.shape == (2,)
        assert rnn_states_critic.shape == (1,)

    def test_get_actions_deterministic(self):
        values, actions, action_log_probs, rnn_states_actor, rnn_states_critic = self.model.get_actions(
            self.cent_obs, self.obs, self.rnn_states_actor, self.rnn_states_critic, self.masks, deterministic=True
        )
        assert values.shape == (1,)
        assert actions.shape == (3,)
        assert action_log_probs.shape == (3,)
        assert rnn_states_actor.shape == (2,)
        assert rnn_states_critic.shape == (1,)

    def test_get_actions_with_masks(self):
        masks = np.array([[0]])
        values, actions, action_log_probs, rnn_states_actor, rnn_states_critic = self.model.get_actions(
            self.cent_obs, self.obs, self.rnn_states_actor, self.rnn_states_critic, masks
        )
        assert values.shape == (1,)
        assert actions.shape == (3,)
        assert action_log_probs.shape == (3,)
        assert rnn_states_actor.shape == (2,)
        assert rnn_states_critic.shape == (1,)

    def test_get_actions_empty_obs(self):
        obs = np.array([[]])
        with pytest.raises(ValueError):
            self.model.get_actions(self.cent_obs, obs, self.rnn_states_actor, self.rnn_states_critic, self.masks)