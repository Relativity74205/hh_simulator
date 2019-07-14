import pytest
import numpy as np

import vector_functions as vf


@pytest.mark.parametrize('vec, unit_vec', [
    ([1, 0, 0], [1.0, 0.0, 0.0]),
    ([1.0, 0.0, 0.0], [1.0, 0.0, 0.0]),
    ([1, 0, 0], [1, 0, 0]),
    ([1, 1, 1], 3 * [1/np.sqrt(3)]),
    ([-1, -1, -1], 3 * [-1/np.sqrt(3)]),
    ([1, 2, 3], [1/14**0.5, 2/14**0.5, 3/14**0.5]),
    ([0, 0, 0], [0, 0, 0])
])
def test_get_unit_vector(vec, unit_vec):
    vec = np.array(vec)
    unit_vec = np.array(unit_vec)

    np.testing.assert_array_equal(vf.get_unit_vector(vec),
                                  unit_vec)


@pytest.mark.parametrize('vec, vec_len', [
    ([1, 0, 0], 1),
    [[0, 0, 0], 0],
    [[1, 1, 1], np.sqrt(3)],
    [(1, 2, 3), np.sqrt(14)]
])
def test_get_vector_length(vec, vec_len):
    vec = np.array(vec)
    assert vf.get_vector_length(vec) == vec_len
