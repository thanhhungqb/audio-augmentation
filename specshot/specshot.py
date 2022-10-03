import torch.nn as nn
import torch


class SpecShot(nn.Module):
    """_summary_

    Args:
        mask_ratio (float): fraction of number of masked pixels per total pixels.
        mask_value (float): value of masked pixels.
    """
    
    def __init__(self, mask_ratio=0.3, mask_value=0.0):
        super().__init__()

        self.mask_ratio = mask_ratio
        self.mask_value = mask_value

    @torch.no_grad()
    def forward(self, input_spec):
        batch_size, freq_size, time_size = input_spec.shape
        prob = -1.0 * torch.rand(batch_size, freq_size, time_size) + 1.0
        mask = prob > self.mask_ratio
        input_spec = input_spec * mask.to(input_spec.device)
        return input_spec
