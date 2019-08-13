import pytest
import numpy as np

from SpaceShip import SpaceShip
from SpaceShip import get_ship_length, get_cnt_broadside_parts, get_weapon_systems, \
    get_defense_val, get_surplus_weapons_array, get_ship_parts
import global_parameters as paras
from space_objects import ships
from Weapon import ShipWeapons

zero_vec = np.zeros(3)


@pytest.fixture
def hms_objects():
    name = 'test_ship'
    hms = SpaceShip(name)
    hms_dict = ships[name]

    return hms, hms_dict


def test_space_ship(hms_objects):
    hms, hms_dict = hms_objects

    assert isinstance(hms, SpaceShip)
    assert hms.mass == hms_dict['mass']
    assert hms.size == hms_dict['size']
    assert hms.values_max == hms_dict['max_values']
    assert not hms.orientation
    assert not hms.orientation_velocity
    assert not hms.orientation_acceleration
    assert not hms.rotation
    assert not hms.rotation_velocity
    assert not hms.rotation_acceleration
    assert hms.compartment_health_max == hms_dict['compartment_health']
    assert hms.ship_length == 6
    assert len(hms.compartments) == 0
    assert isinstance(hms.weapons, ShipWeapons)
    assert len(hms.weapons.weapon_systems) == 0


def test_space_ship_bad():
    with pytest.raises(KeyError):
        SpaceShip('bla')


def test_init_parameters_default(hms_objects):
    hms, _ = hms_objects
    hms.init_parameters()
    np.testing.assert_array_equal(hms.orientation, zero_vec)
    np.testing.assert_array_equal(hms.orientation_velocity, zero_vec)
    np.testing.assert_array_equal(hms.orientation_acceleration, zero_vec)
    assert hms.rotation == 0
    assert hms.rotation_velocity == 0
    assert hms.rotation_acceleration == 0
    assert len(hms.compartments) > 0
    assert len(hms.weapons) > 0


def test_init_parameters(hms_objects):
    hms, _ = hms_objects
    assert False


def test_create_compartments(hms_objects):
    hms, _ = hms_objects
    assert False


@pytest.mark.parametrize('pos_x, pos_y, ship_part_x, ship_part_y', [

])
def test_create_compartment(hms_objects, pos_x, pos_y, ship_part_x, ship_part_y):
    hms, _ = hms_objects
    compartment = hms.create_compartment(pos_x, pos_y, ship_part_x, ship_part_y)

    assert not compartment


@pytest.mark.parametrize('ship_length, ship_parts', [
    (2, ['bow', 'stern']),
    (3, ['bow', 'center_1', 'stern']),
    (4, ['bow', 'center_1', 'center_2', 'stern']),
    (6, ['bow', 'center_1', 'center_2', 'center_3', 'center_4', 'stern'])
])
def test_get_ship_parts(ship_length, ship_parts):
    assert get_ship_parts(ship_length) == ship_parts


@pytest.mark.parametrize('ship_length', [
    0,
    1,
    -1
])
def test_create_compartments_bad_case(hms_objects, ship_length):
    hms, _ = hms_objects
    hms.ship_length = 1
    with pytest.raises(ValueError):
        hms.create_compartments()


def test_add_weapons():
    assert False


def test_create_weapon(hms_objects):
    hms, _ = hms_objects
    hms.create_weapon('test_beam', 'bow', 0)
    assert len(hms.weapons.weapon_systems) == 1
    assert not hms.compartments
    hms.create_weapon('test_beam', 'bow', 0)
    assert len(hms.weapons.weapon_systems) == 2
    assert not hms.compartments


def test_add_weapon_to_compartment():
    assert False


def test_create_compartment_defense(hms_objects):
    assert False


@pytest.mark.parametrize('weapons_cnt, cnt_broadside_parts, cnt_weapons_part, surplus_arr', [
    (10, 4, 2, [0, 3]),
    (2, 4, 0, [0, 3]),
    (8, 4, 2, []),
    (8, 8, 1, []),
    (7, 8, 0, [0, 1, 2, 3, 5, 6, 7]),
    (6, 8, 0, [0, 1, 2, 5, 6, 7]),
    (5, 8, 0, [0, 2, 3, 5, 7]),
    (4, 8, 0, [0, 2, 5, 7]),
    (3, 8, 0, [1, 3, 6]),
    (2, 8, 0, [1, 6]),
    (1, 8, 0, [3]),
    (6, 7, 0, [0, 1, 2, 4, 5, 6]),
    (5, 7, 0, [0, 1, 3, 5, 6]),
    (4, 7, 0, [0, 2, 4, 6]),
    (3, 7, 0, [1, 3, 5]),
    (2, 7, 0, [1, 5]),
    (1, 7, 0, [3]),
    (0, 4, 0, []),
    (0, 0, 0, []),
    [2, 0, 0, []]
])
def test_get_surplus_weapons_array(weapons_cnt, cnt_broadside_parts, cnt_weapons_part, surplus_arr):
    assert get_surplus_weapons_array(weapons_cnt, cnt_broadside_parts) == (cnt_weapons_part, surplus_arr)


@pytest.mark.parametrize('size_dict_length, ship_length_units', [
    (300, 3),
    (350, 3),
    (399, 3),
    (401, 4),
    (200, 2),
    (199, ValueError),
    (1, ValueError),
    (0, ValueError),
    (-1, ValueError)
])
def test_get_ship_length(size_dict_length, ship_length_units):
    size_dict = {'length': size_dict_length,
                 'height': 100,
                 'width': 100
                 }
    if ship_length_units == ValueError:
        with pytest.raises(ValueError):
            get_ship_length(size_dict)
    else:
        assert get_ship_length(size_dict) == ship_length_units


@pytest.mark.parametrize('ship_length, broadside_parts', [
    (3, 1),
    (4, 2),
    (2, 0)
])
def test_get_cnt_broadside_parts(ship_length, broadside_parts):
    assert get_cnt_broadside_parts(ship_length) == broadside_parts


def test_get_defense_val():
    assert False


@pytest.mark.parametrize('orientation, weapon_systems', [
    ('left', [1]),
    ('right', [1]),
    ('bow', [2]),
    ('stern', [3]),
    ('asd', ValueError)
])
def test_get_weapon_systems(orientation, weapon_systems):
    weapons_dict = {'broadside': [1],
                    'bow': [2],
                    'stern': [3]
                    }
    if weapon_systems == ValueError:
        with pytest.raises(ValueError):
            get_weapon_systems(orientation, weapons_dict)
    else:
        assert get_weapon_systems(orientation, weapons_dict) == weapon_systems
