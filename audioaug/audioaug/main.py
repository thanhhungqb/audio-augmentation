import sys
import yaml
from class_choices import perturbation_choices

def get_normal_perturbation(config):
    perturbation_class = config['perturbation']
    perturbation_class = perturbation_choices.get(perturbation_class)
    perturbation_conf = config.get('perturbation_conf', {})
    perturbation = perturbation_class(**perturbation_conf)
    return perturbation

def get_perturbation(config):
    perturbation_class = perturbation_choices.get(config['perturbation'])

    perturbation_conf = config.get('perturbation_conf', {})
    for k in perturbation_conf:
        if k == 'transformers':
            perturbation_conf[k] = list(map(get_perturbation, perturbation_conf[k]))

    perturbation = perturbation_class(**perturbation_conf)

    return perturbation

def main(config_file):
    with open(config_file, 'r') as f:
        config = yaml.load(f, Loader=yaml.Loader)
    path = config['path']
    outpath = config['outpath']
    nj = config['nj']
    # perturbation_class = perturbation_choices.get(config.get('perturbation'))
    # perturbation_conf = config.get('perturbation_conf', {})
    # if config.get('perturbation') == 'rand_perturbation':
    #     perturbation_conf['transformers'] = list(map(get_normal_perturbation, perturbation_conf['transformers']))

    # perturbation = peget_normal_perturbation(config)

    perturbation = get_perturbation(config)

    perturbation(path, outpath, nj)


if __name__ == '__main__':
    main(sys.argv[1])
            

            

