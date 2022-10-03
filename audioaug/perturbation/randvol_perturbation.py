from typing import Optional, Sequence, Union
import numpy as np
from perturbation.abs_perturbation import AbsPerturbation

class RandVolume(AbsPerturbation):
    """
    This perturbation will randomly choose some positions for changing volume. At each position, it will span to some next positions to make the same changing effect.
    Args:
        - Required argument:
            `num_pos`: Number of start position
            `min_span`: Minimum span at each position
            `max_span`: Maximun span at each postion 
            `min_ratio`: Minimum change of volume (in amplitude)
            `max_ratio`: Maximum change of volume (in amplitude)
    """
    def __init__(
        self, 
        num_pos: int = 50, 
        min_span: Union[float, int] = 0.01, 
        max_span: Union[float, int] = 0.1,
        min_ratio: Union[float, int] = 0.1,
        max_ratio: Union[float, int] = 10.0, 
        *args, **kwargs
    ):
        super(RandVolumeFixedNumOfRegions, self).__init__(*args, **kwargs)
        assert type(min_span) == type(max_span), "`min_span` and `max_span` must have the same type (float or int)"
        assert min_span < max_span, "`min_span` must be lower than `max_span`"
        assert min_ratio < max_ratio, "`min_ratio` must be lower than `max_ratio`"
        if isinstance(min_span, float):
            assert min_span > 0 and min_span < 1
        if isinstance(max_span, float):
            assert max_span > 0 and min_span < 1
        self.num_pos = num_pos
        self.min_span = min_span
        self.max_span = max_span
        self.min_ratio = min_ratio
        self.max_ratio = max_ratio

    def transform_signal(self, signal, sr_in):
        """
        Args:
            signal: input waveform (T, )
        Returns:
            signal_out: Batch of pertubated waveform (T,)            
        """
        T = signal.shape[0]

        # Calculate the real span (float -> int)
        if isinstance(self.min_span, float):
            min_span = int(T * self.min_span)
        else:
            min_span = self.min_span

        if isinstance(self.max_span, float):
            max_span = int(T * self.max_span)
        else:
            max_span = self.max_span 

        # spans: (num_pos, 1)
        spans = np.expand_dims(np.random.randint(
            min_span, 
            max_span, 
            (self.num_pos,)
        ), 1)
        
        # pos: (num_pos, 1)
        pos = np.expand_dims(np.random.randint(
            0, max(1, T - spans.max()), 
            (self.num_pos,),
        ), 1)

        # ratios: (num_pos, 1): How much volume is changed at each span
        ratios = (self.min_ratio - self.max_ratio) * np.random.uniform(size=pos.shape) + self.max_ratio
        # aran: (1, L)
        aran = np.arange(T)[None, :]

        # pertub_map: (num_pos, L) 
        # If True: volume pertubation is applied
        pertub_map = ((pos <= aran) * (aran < (pos + spans)))

        ones = np.ones(pos.shape)
        # vol_adjustment: (num_pos, L)
        vol_adjustment = pertub_map * (ratios - ones) 
        vol_adjustment = vol_adjustment * np.expand_dims(signal, 0)

        # non_zero_per_timestep: (L,)
        num_nonzeros = np.count_nonzero(pertub_map, 0)
        
        # vol_adjustment: (num_pos, L) -> (L)
        vol_adjustment = vol_adjustment.sum(axis=0)/(num_nonzeros + 1e-7)

        return vol_adjustment + signal
