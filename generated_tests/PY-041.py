import pytest
import torch
from unittest.mock import MagicMock

class TestPPOUpdate:
    def setup_method(self):
        self.ppo = MagicMock()
        self.ppo.policy.actor_optimizer = MagicMock()
        self.ppo.policy.critic_optimizer = MagicMock()
        self.ppo.policy.evaluate_actions = MagicMock(return_value=(torch.tensor(1.0), torch.tensor(1.0), torch.tensor(1.0)))
        self.ppo.cal_value_loss = MagicMock(return_value=torch.tensor(1.0))
        self.ppo._use_policy_active_masks = True
        self.ppo._use_max_grad_norm = True
        self.ppo.max_grad_norm = 1.0
        self.ppo.entropy_coef = 0.01
        self.ppo.value_loss_coef = 0.5
        self.ppo.tpdv = {'dtype': torch.float32}

    def test_ppo_update_with_actor_update(self):
        sample = (torch.zeros(1, 10), torch.zeros(1, 10), torch.zeros(1, 10), 
                  torch.zeros(1, 10), torch.zeros(1, 10), torch.zeros(1, 10), 
                  torch.zeros(1, 10), torch.zeros(1, 10), torch.zeros(1, 10), 
                  torch.zeros(1, 10), torch.zeros(1, 10), torch.zeros(1, 10), 
                  torch.zeros(1, 10))
        value_loss, critic_grad_norm, policy_loss, dist_entropy, actor_grad_norm, imp_weights = self.ppo.ppo_update(sample, update_actor=True)

        assert isinstance(value_loss, torch.Tensor)
        assert isinstance(critic_grad_norm, torch.Tensor)
        assert isinstance(policy_loss, torch.Tensor)
        assert isinstance(dist_entropy, torch.Tensor)
        assert isinstance(actor_grad_norm, torch.Tensor)
        assert isinstance(imp_weights, torch.Tensor)

    def test_ppo_update_without_actor_update(self):
        sample = (torch.zeros(1, 10), torch.zeros(1, 10), torch.zeros(1, 10), 
                  torch.zeros(1, 10), torch.zeros(1, 10), torch.zeros(1, 10), 
                  torch.zeros(1, 10), torch.zeros(1, 10), torch.zeros(1, 10), 
                  torch.zeros(1, 10), torch.zeros(1, 10), torch.zeros(1, 10), 
                  torch.zeros(1, 10))
        value_loss, critic_grad_norm, policy_loss, dist_entropy, actor_grad_norm, imp_weights = self.ppo.ppo_update(sample, update_actor=False)

        assert isinstance(value_loss, torch.Tensor)
        assert isinstance(critic_grad_norm, torch.Tensor)
        assert isinstance(policy_loss, torch.Tensor)
        assert isinstance(dist_entropy, torch.Tensor)
        assert isinstance(actor_grad_norm, torch.Tensor)
        assert isinstance(imp_weights, torch.Tensor)

    def test_ppo_update_with_active_masks(self):
        self.ppo._use_policy_active_masks = True
        sample = (torch.zeros(1, 10), torch.zeros(1, 10), torch.zeros(1, 10), 
                  torch.zeros(1, 10), torch.zeros(1, 10), torch.zeros(1, 10), 
                  torch.zeros(1, 10), torch.zeros(1, 10), torch.ones(1, 10), 
                  torch.zeros(1, 10), torch.zeros(1, 10), torch.zeros(1, 10), 
                  torch.zeros(1, 10))
        value_loss, critic_grad_norm, policy_loss, dist_entropy, actor_grad_norm, imp_weights = self.ppo.ppo_update(sample, update_actor=True)

        assert isinstance(value_loss, torch.Tensor)
        assert isinstance(critic_grad_norm, torch.Tensor)

    def test_ppo_update_without_active_masks(self):
        self.ppo._use_policy_active_masks = False
        sample = (torch.zeros(1, 10), torch.zeros(1, 10), torch.zeros(1, 10), 
                  torch.zeros(1, 10), torch.zeros(1, 10), torch.zeros(1, 10), 
                  torch.zeros(1, 10), torch.zeros(1, 10), torch.ones(1, 10), 
                  torch.zeros(1, 10), torch.zeros(1, 10), torch.zeros(1, 10), 
                  torch.zeros(1, 10))
        value_loss, critic_grad_norm, policy_loss, dist_entropy, actor_grad_norm, imp_weights = self.ppo.ppo_update(sample, update_actor=True)

        assert isinstance(value_loss, torch.Tensor)
        assert isinstance(critic_grad_norm, torch.Tensor)

    def test_ppo_update_with_max_grad_norm(self):
        self.ppo._use_max_grad_norm = True
        sample = (torch.zeros(1, 10), torch.zeros(1, 10), torch.zeros(1, 10), 
                  torch.zeros(1, 10), torch.zeros(1, 10), torch.zeros(1, 10), 
                  torch.zeros(1, 10), torch.zeros(1, 10), torch.ones(1, 10), 
                  torch.zeros(1, 10), torch.zeros(1, 10), torch.zeros(1, 10), 
                  torch.zeros(1, 10))
        value_loss, critic_grad_norm, policy_loss, dist_entropy, actor_grad_norm, imp_weights = self.ppo.ppo_update(sample, update_actor=True)

        assert isinstance(value_loss, torch.Tensor)
        assert isinstance(critic_grad_norm, torch.Tensor)

    def test_ppo_update_without_max_grad_norm(self):
        self.ppo._use_max_grad_norm = False
        sample = (torch.zeros(1, 10), torch.zeros(1, 10), torch.zeros(1, 10), 
                  torch.zeros(1, 10), torch.zeros(1, 10), torch.zeros(1, 10), 
                  torch.zeros(1, 10), torch.zeros(1, 10), torch.ones(1, 10), 
                  torch.zeros(1, 10), torch.zeros(1, 10), torch.zeros(1, 10), 
                  torch.zeros(1, 10))
        value_loss, critic_grad_norm, policy_loss, dist_entropy, actor_grad_norm, imp_weights = self.ppo.ppo_update(sample, update_actor=True)

        assert isinstance(value_loss, torch.Tensor)
        assert isinstance(critic_grad_norm, torch.Tensor)