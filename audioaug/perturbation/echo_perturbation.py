from perturbation.abs_perturbation import AbsPerturbation

import sox
import random
import numpy as np

class Echo(AbsPerturbation):
    def __init__(self, gain_in=1.0, gain_out=1.0, n_echos_max=1, min_delay=30, max_delay=60, min_decay=0.1, max_decay=0.4, *args, **kwargs):
        super(Echo, self).__init__(*args, **kwargs)
        self.gain_in = gain_in
        self.gain_out = gain_out
        self.n_echos_max = n_echos_max
        self.min_delay = min_delay
        self.max_delay = max_delay 
        self.min_decay = min_decay
        self.max_decay = max_decay
        
    def transform_signal(self, signal, sr_in):
        n_echos = np.random.randint(1, self.n_echos_max + 1)

        delays = np.random.uniform(self.min_delay, self.max_delay, size=n_echos).tolist()
        decays = np.random.uniform(self.min_decay, self.max_decay, size=n_echos).tolist()

        trfm = sox.Transformer()

        trfm.echo(self.gain_in, self.gain_out, n_echos, delays, decays)

        return trfm.build_array(input_array=signal, sample_rate_in=sr_in)