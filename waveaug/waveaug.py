import os
import sox
import numpy as np
import random
import soundfile as sf
import librosa
from tqdm import tqdm
import argparse


def add_noise(noise_list, signal):
  """_summary_

  Args:
      noise_list (numpy array): list of multiple noises which are numpy array.
      signal (numpy array).
  """   
  
  signal_length = len(signal)
  
  # extract noise from noise list
  noise = random.choice(noise_list)
  start = random.randint(0, len(noise) - signal_length - 1)
  noise = noise[start:start + signal_length]
        
  # calculate power of audio and noise
  snr = random.randint(5, 15)
  signal_energy = np.mean(signal**2)
  noise_energy = np.mean(noise**2)
  coef = np.sqrt(10.0 ** (-snr/10) * signal_energy / noise_energy)
  signal_coef = np.sqrt(1 / (1 + coef**2))
  noise_coef = np.sqrt(coef**2 / (1 + coef**2))
        
  return signal_coef * signal + noise_coef * noise


def volume(n_segments, min_relative_vol, max_relative_vol):
  """_summary_
  
  Args:
      n_segments (int): number of segment that audio will be segmented.
      min_relative_vol (float): minimum volume of audio (over 0.0).
      max_relative_vol (float): maximum volume of audio (over min_relative_vol).
  Returns:
      function: require a siganl (numpy array as input).
  """

  assert (n_segments > 0) and (min_relative_vol > 0) and (max_relative_vol > 0)
  def exec(signal):
    signal_length = len(signal)
    win_length = int(signal_length/n_segments)
    segments = None
    for idx in range(n_segments):
      start = idx * win_length
      if idx < n_segments - 1:
        segment = signal[start:start + win_length]
      else:
        segment = signal[start:signal_length]
      scale = np.random.uniform(min_relative_vol, max_relative_vol)
      segment = scale * segment
      if idx == 0:
        segments = segment
      else:
        segments = np.concatenate((segments, segment))
    return segments
  return exec


def perturb(n_effects, sample_rate=16000):
  """_summary_

  Args:
      n_effects (int): number of effect will be applied on a signal.
      sr (int, optional): Defaults to 16000.
  Returns:
      function: require a siganl (numpy array as input).
  """

  def exec(signal):
    effects = ['echo', 'speed', 'pitch', 'volume']
    transforms = np.random.choice(effects, size=n_effects, replace=False)
    for transform in transforms:
      if transform == 'speed':
        value = np.random.choice([0.5, 1.1]) + np.random.uniform(0.0, 0.4)
        tfm = sox.Transformer()
        tfm.speed(value)
        signal = tfm.build_array(input_array=signal, sample_rate_in=sample_rate)
      elif transform == 'pitch':
        value = np.random.choice([-10, 2]) + np.random.randint(0, 8)
        tfm = sox.Transformer()
        tfm.pitch(value)
        signal = tfm.build_array(input_array=signal, sample_rate_in=sample_rate)
      elif transform == 'echo':
        n_echos = np.random.randint(1, 3)
        delays = [60] * n_echos
        decays = [0.4] * n_echos
        tfm = sox.Transformer()
        tfm.echo(gain_in=1.0, gain_out=1.0, n_echos=n_echos, delays=delays, decays=decays)
        signal = tfm.build_array(input_array=signal, sample_rate_in=sample_rate)
      else:
        n_segments = np.random.randint(2, 4)
        min_vol = 0.4
        max_vol = 10
        vol = volume(n_segments=n_segments, min_relative_vol=min_vol, max_relative_vol=max_vol)
        signal = vol(signal)
    return signal
  return exec


def build_dataset(in_path, out_path, noise_list, n_perturbs, n_disturbs, max_effect=3, sample_rate=16000):
  """_summary_

  Args:
      in_path (str): path to source.
      out_path (str): path to destination.
      noise_list (numpy array): list of noises which are numpy array.
      max_effect (int, optional): Defaults to 3.
      n_perturbs (int): number of times applying perturbation.
      n_disturbs (int): number of times applying disturbance.
      sample_rate (int, optional): Defaults to 16000.
  """

  waves = librosa.util.find_files(in_path, ext='wav')
  
  for wav in tqdm(waves):
    signal, sr = librosa.load(wav, sr=sample_rate)
    splt = wav.split('/')
    name = splt[-1][:-4]
    
    # clean
    clean_dir = os.path.join(out_path, name + '.wav')
    sf.write(clean_dir, signal, samplerate=sample_rate)

    # perturbation
    for i in range(n_perturbs):
      n_effects = np.random.randint(1, max_effect)
      transform = perturb(n_effects=n_effects)
      perturb_signal = transform(signal)
      perturb_name = name + f'_perturb_{i}.wav'
      perturb_dir = os.path.join(out_path, perturb_name)
      sf.write(perturb_dir, perturb_signal, samplerate=sample_rate)
    
    # disturbance
    for i in range(n_disturbs):
      noise_signal = add_noise(noise_list=noise_list, signal=signal)
      noise_name = name + f'_noise_{i}.wav'
      noise_dir = os.path.join(out_path, noise_name)
      sf.write(noise_dir, noise_signal, samplerate=sample_rate)
    

def build_prompts(in_prompts_path, out_prompts_path, n_perturbs, n_disturbs,):
  """_summary_

  Args:
      in_prompts_path (str): path of source prompts.
      out_prompts_path (str): path of destination prompts.
      n_perturbs (int): number of times applying perturbation.
      n_disturbs (int): number of times applying disturbance.
  """

  with open(in_prompts_path, 'r') as fin:
    with open(out_prompts_path, 'w') as fout:
      for line in fin:
        splt = line.split()
        name = splt[0]
        label = ' '.join(splt[1:])
        fout.write(name + ' ' + label + '\n')
        for i in range(n_perturbs):
          fout.write(name + f'_perturb_{i}' + ' ' + label + '\n')
        for i in range(n_disturbs):
          fout.write(name + f'_noise_{i}' + ' ' + label + '\n')


def main():
  parser = argparse.ArgumentParser()
  parser.add_argument('src', type=str)
  parser.add_argument('dst', type=str)
  parser.add_argument('n_perturbs', type=int)
  parser.add_argument('n_disturbs', type=int)
  args = parser.parse_args()
  src = args.src
  dst = args.dst
  n_perturbs = args.n_perturbs
  n_disturbs = args.n_disturbs
  
  new_waves_dir = os.path.join(dst, 'waves')
  os.mkdir(new_waves_dir)
  
  noise_path = './audio-augmentation/audioaug/noise.npy'
  noise_list = np.load(noise_path, allow_pickle=True)
  
  build_dataset(
    in_path=src, 
    out_path=new_waves_dir,
    noise_list=noise_list,
    n_perturbs=n_perturbs,
    n_disturbs=n_disturbs,
    max_effect=3,
    sample_rate=16000
    )
  
  txts = librosa.util.find_files(src, ext='txt')
  if len(txts) == 0:
    raise Exception('Source directory must include prompts.txt')
  
  found = False
  for dir in txts:
    if "prompts.txt" in dir:
      in_prompts_path = dir
      found = True
      break
  if not found:
    raise Exception('Source directory must include prompts.txt')
  
  out_prompts_path = os.path.join(dst, 'prompts.txt')
  
  build_prompts(
    in_prompts_path=in_prompts_path,
    out_prompts_path=out_prompts_path,
    n_perturbs=n_perturbs,
    n_disturbs=n_disturbs
  )


if __name__ == '__main__':
  main()
