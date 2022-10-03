import os
import soundfile as sf
import sox
from tqdm import tqdm
from joblib import Parallel, delayed

class AbsPerturbation:
    def __init__(self, sr=None, channel=None):
        self.sr = sr
        self.channel = channel

        # Formatter used for __call__(), if not set, __call__() cannot be used
        if self.channel is not None and self.sr is not None:
            self.formatter = self.build_formatter()
        else:
            self.formatter = None

    def build_formatter(self):
        formatter = sox.Transformer()
        # formatter.rate(self.sr)
        # formatter.channels(self.channel)
        formatter.set_output_format(rate=self.sr, channels=self.channel)
        return formatter

    def transform_signal(self, signal, sr_in):
        """
        Returns:
            signal: transformed signal
        """
        raise NotImplementedError

    def call_file(self, audio_file, outfile):
        if os.path.exists(outfile):
            # Check saving to the same orig file
            assert not os.path.samefile(audio_file, outfile)
            # Otherwise, do nothing
            return
            
        # Make directory if not exists
        outdir = os.path.dirname(outfile)
        os.makedirs(outdir, exist_ok=True)

        aud, sr_in = sf.read(audio_file)
        
        # Transform audio signal
        aud = self.transform_signal(aud, sr_in)

        # Format output audio
        aud = self.formatter.build_array(input_array=aud, sample_rate_in=sr_in)

        sf.write(outfile, aud, self.sr)

        return

        # self.formatter.build_file(input_array=aud, sample_rate_in=sr_in, output_filepath=outfile)

    def call_directory(self, audio_dir, outdir, nj=1):
        def process_file(f):
            if f.endswith('.wav'):
                out_subdir = os.path.relpath(root, audio_dir)
                self.call_file(os.path.join(root, f), os.path.join(outdir, out_subdir, f))

        # Make directory if not exists
        os.makedirs(outdir, exist_ok=True)
        assert not os.path.samefile(audio_dir, outdir)

        for root, dirs, files in tqdm(os.walk(audio_dir)):
            # for f in tqdm(files):
            #     if f.endswith('.wav'):
            #         out_subdir = os.path.relpath(root, audio_dir)
            #         self.call_file(os.path.join(root, f), os.path.join(outdir, out_subdir, f))

            Parallel(n_jobs=nj)(delayed(process_file)(f) for f in tqdm(files))

    def __call__(self, path, outpath, nj=1):
        if os.path.isdir(path):
            self.call_directory(path, outpath, nj)
        # nj is not used when path is a file
        elif os.path.isfile(path):
            self.call_file(path, outpath)
        else:
            raise ValueError('path must be a file or directory')