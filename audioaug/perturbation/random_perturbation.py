import glob
import os
import numpy as np
import soundfile as sf
from perturbation.abs_perturbation import AbsPerturbation

class RandomPerturbation(AbsPerturbation):
    def __init__(self, transformers, min_transformers=0, max_transformers=1, *args, **kwargs):
        super(RandomPerturbation, self).__init__(*args, **kwargs)
        self.min_transformers = min_transformers
        self.max_transformers = max_transformers
        self.transformers = transformers

    def transform_signal(self, signal, sr_in):
        # Get number of transformation
        sample_num_transformers = np.random.randint(self.min_transformers, self.max_transformers + 1)

        # Choose transformations
        # Should we apply the same transformation (means replace=True)?
        transformers = np.random.choice(self.transformers, sample_num_transformers, replace=False)
        for trfm in transformers:
            signal = trfm.transform_signal(signal, sr_in)

        return signal