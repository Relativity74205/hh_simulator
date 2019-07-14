import pytest
import numpy as np

from SpaceObject import SpaceObject
import global_parameters as paras


zero_vec = np.zeros(3)
ship_dict = {'size': [100, 20, 20],
             'mass': 50000,
             'max_values': {'velocity': 100000,
                            'acceleration': 500,
                            'orientation_velocity': 0.5,
                            'orientation_acceleration': 0.1,
                            'rotation_velocity': 0.5,
                            'rotation_acceleration': 0.1
                            }}


def test_spaceobject():
    so = SpaceObject(**ship_dict)

    assert so.size == [100, 20, 20]
    assert so.mass == 50000
    assert so.max_velocity == 100000
    assert so.max_acceleration == 500
    assert so.max_orientation_velocity == 0.5
    assert so.max_orientation_acceleration == 0.1
    assert so.max_rotation_velocity == 0.5
    assert so.max_rotation_acceleration == 0.1


@pytest.mark.parametrize('pos, v', [
    ([0, 0, 0], [1, 0, 0])
])
def test_spaceobject_init(pos, v):
    pos = np.array(pos)
    v = np.array(v)
    so = SpaceObject(**ship_dict)
    so.init_parameters(position=pos, velocity=v)
    np.testing.assert_array_equal(pos, so.position)
    np.testing.assert_array_equal(v, so.velocity)
    np.testing.assert_array_equal(zero_vec, so.acceleration)


@pytest.mark.parametrize('time_delta, start_pos, start_v, a, a_vec, end_pos, end_v', [
    (1.0, zero_vec, zero_vec, 1., [1., 0., 0.], [0.5, 0., 0.], [1., 0., 0.]),
    (10.0, zero_vec, zero_vec, 1., [1., 0., 0.], [50., 0., 0.], [10., 0., 0.]),
    (1.0, [0.5, 0., 0.], [1., 0., 0.], 1., [1., 0., 0.], [2, 0., 0.], [2., 0., 0.]),
    (1.0, [0.5, 0., 0.], [1., 0., 0.], 1., [-1., 0., 0.], [1, 0., 0.], [0., 0., 0.])
])
def test_spaceobject_move(time_delta, start_pos, start_v, a, a_vec, end_pos, end_v):
    paras.TIMEDELTA_MOVE = time_delta
    so = SpaceObject(**ship_dict)
    start_pos = np.array(start_pos)
    start_v = np.array(start_v)
    a_vec = np.array(a_vec)
    end_pos = np.array(end_pos)
    end_v = np.array(end_v)

    so.init_parameters(position=start_pos, velocity=start_v)
    so.set_acceleration(a, a_vec)
    so.move()
    np.testing.assert_array_equal(end_pos, so.position)
    np.testing.assert_array_equal(end_v, so.velocity)


@pytest.mark.parametrize('acceleration, vec, accel_vec', [
    (1, [1, 0, 0], [1, 0, 0]),
    (500, [1, 0, 0], [500, 0, 0]),
    (501, [1, 0, 0], [500, 0, 0]),
    (0, [1, 0, 0], [0, 0, 0]),
    (1, [0, 0, 0], [0, 0, 0])
])
def test_spaceobject_set_acceleration(acceleration, vec, accel_vec):
    vec = np.array(vec)
    accel_vec = np.array(accel_vec)

    so = SpaceObject(**ship_dict)
    so.set_acceleration(acceleration, vec)

    np.testing.assert_array_equal(accel_vec,
                                  so.acceleration)
