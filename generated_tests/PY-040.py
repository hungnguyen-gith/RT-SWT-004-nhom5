import pytest
import torch

class TestCalValueLoss:
    class MockModel:
        def __init__(self, use_popart=False, use_valuenorm=False, use_huber_loss=False, 
                     use_clipped_value_loss=False, use_value_active_masks=False, 
                     clip_param=0.2, huber_delta=1.0):
            self._use_popart = use_popart
            self._use_valuenorm = use_valuenorm
            self._use_huber_loss = use_huber_loss
            self._use_clipped_value_loss = use_clipped_value_loss
            self._use_value_active_masks = use_value_active_masks
            self.clip_param = clip_param
            self.huber_delta = huber_delta
            self.value_normalizer = self.MockValueNormalizer()

        class MockValueNormalizer:
            def normalize(self, x):
                return x

    def test_value_loss_no_masks(self):
        model = self.MockModel()
        values = torch.tensor([1.0, 2.0])
        value_preds_batch = torch.tensor([1.0, 1.5])
        return_batch = torch.tensor([1.0, 2.0])
        active_masks_batch = torch.tensor([1.0, 1.0])
        loss = model.cal_value_loss(values, value_preds_batch, return_batch, active_masks_batch)
        assert loss.item() >= 0

    def test_value_loss_with_masks(self):
        model = self.MockModel(use_value_active_masks=True)
        values = torch.tensor([1.0, 2.0])
        value_preds_batch = torch.tensor([1.0, 1.5])
        return_batch = torch.tensor([1.0, 2.0])
        active_masks_batch = torch.tensor([1.0, 0.0])
        loss = model.cal_value_loss(values, value_preds_batch, return_batch, active_masks_batch)
        assert loss.item() >= 0

    def test_value_loss_huber(self):
        model = self.MockModel(use_huber_loss=True)
        values = torch.tensor([1.0, 2.0])
        value_preds_batch = torch.tensor([1.0, 1.5])
        return_batch = torch.tensor([1.0, 2.0])
        active_masks_batch = torch.tensor([1.0, 1.0])
        loss = model.cal_value_loss(values, value_preds_batch, return_batch, active_masks_batch)
        assert loss.item() >= 0

    def test_value_loss_clipped(self):
        model = self.MockModel(use_clipped_value_loss=True)
        values = torch.tensor([1.0, 2.0])
        value_preds_batch = torch.tensor([1.0, 1.5])
        return_batch = torch.tensor([1.0, 2.0])
        active_masks_batch = torch.tensor([1.0, 1.0])
        loss = model.cal_value_loss(values, value_preds_batch, return_batch, active_masks_batch)
        assert loss.item() >= 0

    def test_value_loss_popart(self):
        model = self.MockModel(use_popart=True)
        values = torch.tensor([1.0, 2.0])
        value_preds_batch = torch.tensor([1.0, 1.5])
        return_batch = torch.tensor([1.0, 2.0])
        active_masks_batch = torch.tensor([1.0, 1.0])
        loss = model.cal_value_loss(values, value_preds_batch, return_batch, active_masks_batch)
        assert loss.item() >= 0

    def test_value_loss_valuenorm(self):
        model = self.MockModel(use_valuenorm=True)
        values = torch.tensor([1.0, 2.0])
        value_preds_batch = torch.tensor([1.0, 1.5])
        return_batch = torch.tensor([1.0, 2.0])
        active_masks_batch = torch.tensor([1.0, 1.0])
        loss = model.cal_value_loss(values, value_preds_batch, return_batch, active_masks_batch)
        assert loss.item() >= 0