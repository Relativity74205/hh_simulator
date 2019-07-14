import numpy as np


def get_unit_vector(vec):
    vec_len = get_vector_length(vec)
    if vec_len == 0:
        unit_vec = np.array([0, 0, 0])
    else:
        unit_vec = vec / vec_len

    return unit_vec


def get_vector_length(vec):
    return np.sqrt(np.sum(vec ** 2))
