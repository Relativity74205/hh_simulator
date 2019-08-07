import pytest
import numpy as np

from SpaceObject import SpaceObject
import global_parameters as paras


zero_vec = np.zeros(3)
ship_dict = {'name': 'Cruiser',
             'size': [100, 20, 20],
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

    assert so.name == 'Cruiser'
    assert so.size == [100, 20, 20]
    assert so.mass == 50000
    assert so.max_velocity == 100000
    assert so.max_acceleration == 500
    np.testing.assert_array_equal(so.position, zero_vec)
    np.testing.assert_array_equal(so.velocity, zero_vec)
    np.testing.assert_array_equal(so.acceleration, zero_vec)


@pytest.mark.parametrize('time_delta, start_pos, v, v_vec, a, a_vec, end_pos, end_v', [
    (1., zero_vec, 0., zero_vec, 1., [1., 0., 0.], [0.5, 0., 0.], [1., 0., 0.]),
    (10., zero_vec, 0., zero_vec, 1., [1., 0., 0.], [50., 0., 0.], [10., 0., 0.]),
    (1., [0.5, 0., 0.], 1., [1., 0., 0.], 1., [1., 0., 0.], [2, 0., 0.], [2., 0., 0.]),
    (1., [0.5, 0., 0.], 1., [1., 0., 0.], 1., [-1., 0., 0.], [1, 0., 0.], [0., 0., 0.])
])
def test_spaceobject_move(time_delta, start_pos, v, v_vec, a, a_vec, end_pos, end_v):
    paras.TIMEDELTA_MOVE = time_delta
    so = SpaceObject(**ship_dict)
    start_pos = np.array(start_pos)
    v_vec = np.array(v_vec)
    a_vec = np.array(a_vec)
    end_pos = np.array(end_pos)
    end_v = np.array(end_v)

    so.position = start_pos
    so.set_velocity(v, v_vec)
    so.set_acceleration(a, a_vec)
    so.move()
    np.testing.assert_array_equal(end_pos, so.position)
    np.testing.assert_array_equal(end_v, so.velocity)


@pytest.mark.parametrize('a, vec, acceleration', [
    (1, [1, 0, 0], [1, 0, 0]),
    (500, [1, 0, 0], [500, 0, 0]),
    (501, [1, 0, 0], [500, 0, 0]),
    (0, [1, 0, 0], [0, 0, 0]),
    (1, [0, 0, 0], [0, 0, 0]),
    (500, [2, 0, 0], [500, 0, 0]),
    (500, [np.sqrt(2), np.sqrt(2), 0], [np.sqrt(0.5)*500, np.sqrt(0.5)*500, 0]),
])
def test_spaceobject_set_acceleration(a, vec, acceleration):
    vec = np.array(vec)
    acceleration = np.array(acceleration)

    so = SpaceObject(**ship_dict)
    so.set_acceleration(a, vec)

    np.testing.assert_array_equal(zero_vec, so.velocity)
    np.testing.assert_array_equal(acceleration, so.acceleration)


@pytest.mark.parametrize('v, vec, velocity', [
    (1, [1, 0, 0], [1, 0, 0]),
    (100000, [1, 0, 0], [100000, 0, 0]),
    (100001, [1, 0, 0], [100000, 0, 0]),
    (0, [1, 0, 0], [0, 0, 0]),
    (1, [0, 0, 0], [0, 0, 0]),
    (100000, [2, 0, 0], [100000, 0, 0]),
    (100000, [np.sqrt(2), np.sqrt(2), 0], [np.sqrt(0.5)*100000, np.sqrt(0.5)*100000, 0]),
])
def test_spaceobject_set_velocity(v, vec, velocity):
    vec = np.array(vec)
    velocity = np.array(velocity)

    so = SpaceObject(**ship_dict)
    so.set_velocity(v, vec)

    np.testing.assert_array_equal(velocity, so.velocity)
    np.testing.assert_array_equal(zero_vec, so.acceleration)
