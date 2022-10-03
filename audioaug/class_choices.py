from perturbation.random_perturbation import RandomPerturbation
from perturbation.abs_perturbation import AbsPerturbation
from perturbation.randvol_perturbation import RandVolume
from perturbation.pitch_perturbation import Pitch
from perturbation.speed_perturbation import Speed
from perturbation.tempo_perturbation import Tempo
from perturbation.echo_perturbation import Echo

perturbation_choices = {
    'rand_perturbation': RandomPerturbation,
    'randvol': RandVolume,
    'pitch': Pitch,
    'speed': Speed,
    'tempo': Tempo,
    'echo': Echo
}
