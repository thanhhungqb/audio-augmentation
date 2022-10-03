# Audio perturbation

## Instruction for running
```sh
$ main.py /path/to/config.yaml
```

Example configs are located in `example_conf`

## Add new pertubation
1. Inherit class `perturbation.abs_perturbation.AbsPerturbation`. 
2. Implement `transform_signal(signal)` method.
3. Add `(Key, Value)` pair in `class_choices.perturbation_choices`, which  `Value` is perturbation class and `Key` is its identifier (str) that will be used in config file.
4. Fix your bugs, maybe (and my bugs, maybe). :)

## Future plans:
- More perturbations **(not future, NOW)**
- Progress bar
- Add manifest for each perturbated audio
- Checkpoint processed file
