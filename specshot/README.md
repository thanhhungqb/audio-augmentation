## Usage

```
  audio, sample_rate = librosa.load(example_file, sr=16000)
  mel_spec = librosa.feature.melspectrogram(audio, sr=16000)
  specshot = SpecShot(mask_ratio=0.3, mask_value=0.0)
  output = specshot(mel_spec)
```

![Alt text](specshot/melspec_2.png?raw=true "Before applying SpecShot")

![Alt text](specshot/melspec_augment_2.png?raw=true "After applying SpecShot")
