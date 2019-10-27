from .examples_common import *
import numpy as np


def load_diffusion_data():
    """
    Loads the diffusion data.
    """
    data = np.load(os.path.join(example_dir, 'diffusion_data_noise.npy'))
    return data


def load_upperlowercenters_diffusion_data():
    """
    Loads the upper-lower-center diffusion data.
    """
    data = np.load(os.path.join(example_dir, 'diffusion_upperlowercenters_data_noise.npy'))
    return data
