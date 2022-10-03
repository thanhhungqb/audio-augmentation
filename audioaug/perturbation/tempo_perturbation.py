from perturbation.abs_perturbation import AbsPerturbation

import sox
import numpy as np

class Tempo(AbsPerturbation):
    def __init__(self, factor_min=0.5, factor_max=1.5, audio_type=None, quick=False, *args, **kwargs):
        super(Tempo, self).__init__(*args, **kwargs)
        assert factor_min < factor_max
        self.factor_min = factor_min
        self.factor_max = factor_max
        self.audio_type = self.translate_audio_type(audio_type)
        self.quick = quick

    def translate_audio_type(self, audio_type):
        if audio_type is not None:
            if audio_type in ['speech', 's']:
                return 's'
            elif audio_type in ['music', 'm']:
                return 'm'
            elif audio_type in ['linear', 'l']:
                return 'l'
            else:
                raise ValueError('Unknown audio type: {}'.format(audio_type))
        return audio_type

    def transform_signal(self, signal, sr_in):
        factor = np.random.uniform(self.factor_min, self.factor_max)
        trfm = sox.Transformer()
        trfm.tempo(factor, self.audio_type, self.quick)

        return trfm.build_array(input_array=signal, sample_rate_in=sr_in)