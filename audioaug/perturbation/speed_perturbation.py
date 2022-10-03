from perturbation.abs_perturbation import AbsPerturbation

import sox
import numpy as np

class Speed(AbsPerturbation):
    def __init__(self, factor_min=0.5, factor_max=1.5, *args, **kwargs):
        super(Speed, self).__init__(*args, **kwargs)
        assert factor_min < factor_max
        self.factor_min = factor_min
        self.factor_max = factor_max

    def transform_signal(self, signal, sr_in):
        factor = np.random.uniform(self.factor_min, self.factor_max)
        trfm = sox.Transformer()
        trfm.speed(factor)

        return trfm.build_array(input_array=signal, sample_rate_in=sr_in)