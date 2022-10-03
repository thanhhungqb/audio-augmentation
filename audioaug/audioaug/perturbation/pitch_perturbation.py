from perturbation.abs_perturbation import AbsPerturbation

import sox
import numpy as np

class Pitch(AbsPerturbation):
    def __init__(self, n_semitones_min=-5.0, n_semitones_max=5.0, quick=False, *args, **kwargs):
        super(Pitch, self).__init__(*args, **kwargs)
        assert n_semitones_min < n_semitones_max
        self.n_semitones_min = n_semitones_min
        self.n_semitones_max = n_semitones_max
        self.quick = quick

    def transform_signal(self, signal, sr_in):
        n_semitones = np.random.uniform(self.n_semitones_min, self.n_semitones_max)
        trfm = sox.Transformer()
        trfm.pitch(n_semitones, self.quick)

        return trfm.build_array(input_array=signal, sample_rate_in=sr_in)