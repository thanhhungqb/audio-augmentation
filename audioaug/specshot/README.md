## Usage

```
  audio, sample_rate = librosa.load(example_file, sr=16000)
  mel_spec = librosa.feature.melspectrogram(audio, sr=16000)
  specshot = SpecShot(mask_ratio=0.3, mask_value=0.0)
  output = specshot(mel_spec)
```

<p align="center">
  <img src="melspec_2.png" width="350" title="Before applying SpecShot">
  <img src="melspec_augment_2.png" width="350" alt="After applying SpecShot">
</p>