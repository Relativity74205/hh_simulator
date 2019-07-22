import pytest

from SpaceShip import SpaceShip, get_compartments_dict
import global_parameters as paras
from space_objects import ships


@pytest.fixture
def hms_objects():
    name = 'Cruiser'
    hms = SpaceShip(name)
    hms_dict = ships[name]

    return hms, hms_dict


def test_space_ship(hms_objects):
    hms, hms_dict = hms_objects

    assert isinstance(hms, SpaceShip)
    assert hms.mass == hms_dict['mass']
    assert hms.size == hms_dict['size']
    assert hms.max_velocity == hms_dict['max_values']['velocity']
    assert hms.max_acceleration == hms_dict['max_values']['acceleration']
    assert hms.max_orientation_velocity == hms_dict['max_values']['orientation_velocity']
    assert hms.max_orientation_acceleration == hms_dict['max_values']['orientation_acceleration']
    assert hms.max_rotation_velocity == hms_dict['max_values']['rotation_velocity']
    assert hms.max_rotation_acceleration == hms_dict['max_values']['rotation_acceleration']
    assert not hms.orientation
    assert not hms.orientation_velocity
    assert not hms.orientation_acceleration
    assert not hms.rotation
    assert not hms.rotation_velocity
    assert not hms.rotation_acceleration
    assert hms.max_compartment_health == hms_dict['compartment_health']
    assert len(hms.ship_parts) == int(hms_dict['size']['length']/paras.PART_SIZE) + 2
    for _, v in hms.ship_parts.items():
        cs = v['compartments']
        assert len(cs) == 5
        assert {'shield_left', 'hull_left', 'hull_right', 'shield_right'}.issubset(cs.keys())
        for _, c in cs.items():
            assert c is not None


def test_space_ship_bad():
    with pytest.raises(KeyError):
        SpaceShip('bla')


def test_add_weapons():
    assert False


def test_create_compartments(hms_objects):
    pass  # TODO not necessary


@pytest.mark.parametrize('compartment_name, ship_part_name, health, val', [
    ('hull_left', 'bow', 1, 1),
    ('hull_left', 'bow', 2, 2),
    ('shield_left', 'bow', 1, 0),
    ('hull_left', 'bow_shield', 1, 0),
    ('shield_left', 'bow_shield', 1, 0)
])
def test_get_compartment_health(compartment_name, ship_part_name, health, val):
    assert SpaceShip.get_compartment_health(compartment_name, ship_part_name, health) == val


@pytest.mark.parametrize('direction, shields, comp_name, val', [
    ('left', {'broadside': 1}, 'shield_left', 1),
    ('left', {'broadside': 1}, 'shield_right', 0),
    ('right', {'broadside': 1}, 'shield_left', 0),
    ('left', {'broadside': 1}, 'hull_left', 0),
    ('left', {'bow': 1}, 'hull_left', 0),
    ('bow', {'bow': 2, 'stern': 3}, 'bow_shield', 0)
])
def test_get_shield_x(direction, shields, comp_name, val):
    assert SpaceShip.get_shield_x(direction, shields, comp_name) == val


@pytest.mark.parametrize('direction, shields, part_name, val', [
    ('bow', {'bow': 2, 'stern': 3}, 'bow_shield', 2),
    ('stern', {'bow': 2, 'stern': 3}, 'bow_shield', 0),
    ('stern', {'bow': 2, 'stern': 3}, 'stern_shield', 3),
    ('bow', {'bow': 2, 'stern': 3}, 'bow', 0),
    ('bow', {'broadside': 3}, 'bow_shield', 0),
    ('left', {'broadside': 1}, 'shield_left', 0)
])
def test_get_shield_y(direction, shields, part_name, val):
    assert SpaceShip.get_shield_y(direction, shields, part_name) == val


@pytest.mark.parametrize('direction, shields, val', [
    ('top', {'vertical': 1}, 1),
    ('bottom', {'vertical': 1}, 1),
    ('bow', {'vertical', 1}, 0),
    ('top', {'left': 1}, 0)
])
def test_get_shield_z(direction, shields, val):
    assert SpaceShip.get_shield_z(direction, shields) == val


@pytest.mark.parametrize('direction, armor, compartment_name, part_name, val', [
    ('left', {'broadside': 2, 'inner': 1}, 'hull_left', 'bow', 2),
    ('right', {'broadside': 2, 'inner': 1}, 'hull_left', 'bow', 1),
    ('right', {'broadside': 2}, 'hull_left', 'bow', 0),
    ('right', {'broadside': 2, 'inner': 1}, 'hull_right', 'bow', 2),
    ('left', {'broadside': 2, 'inner': 1}, 'hull_left', 'bow_shield', 0),
    ('left', {'broadside': 2, 'inner': 1}, 'shield_left', 'bow', 0),
    ('left', {'broadside': 2, 'inner': 1}, 'middle', 'bow', 1)
])
def test_get_armor_x(direction, armor, compartment_name, part_name, val):
    assert SpaceShip.get_armor_x(direction, armor, compartment_name, part_name) == val


@pytest.mark.parametrize('direction, armor, compartment_name, part_name, val', [
    ('bow', {'bow': 2, 'stern': 3, 'inner': 1}, 'hull_left', 'bow', 2),
    ('bow', {'bow': 2, 'stern': 3, 'inner': 1}, 'middle', 'bow', 2),
    ('stern', {'bow': 2, 'stern': 3, 'inner': 1}, 'hull_left', 'bow', 1),
    ('bow', {'bow': 2, 'stern': 3, 'inner': 1}, 'hull_left', 'stern', 1),
    ('bow', {'bow': 2, 'stern': 3}, 'hull_left', 'stern', 0),
    ('stern', {'bow': 2, 'stern': 3, 'inner': 1}, 'hull_left', 'stern', 3),
    ('bow', {'bow': 2, 'stern': 3, 'inner': 1}, 'middle', 'inner_1', 1),
    ('stern', {'bow': 2, 'stern': 3, 'inner': 1}, 'middle', 'inner_1', 1),
    ('stern', {'bow': 2, 'stern': 3, 'inner': 1}, 'middle', 'bow_shield', 0),
    ('stern', {'bow': 2, 'stern': 3, 'inner': 1}, 'shield_left', 'inner_1', 0)
])
def test_get_armor_y(direction, armor, compartment_name, part_name, val):
    assert SpaceShip.get_armor_y(direction, armor, compartment_name, part_name) == val


@pytest.mark.parametrize('direction, armor, compartment_name, part_name, val', [
    ('top', {'vertical': 2, 'stern': 3, 'inner': 1}, 'hull_left', 'bow', 2),
    ('left', {'vertical': 2, 'stern': 3, 'inner': 1}, 'hull_left', 'bow', 0),
    ('top', {'stern': 3, 'inner': 1}, 'hull_left', 'bow', 0),
    ('bottom', {'vertical': 2, 'stern': 3, 'inner': 1}, 'hull_left', 'bow', 2),
    ('bottom', {'vertical': 2, 'stern': 3, 'inner': 1}, 'hull_left', 'bow_shield', 0),
    ('bottom', {'vertical': 2, 'stern': 3, 'inner': 1}, 'shield_left', 'bow', 0)
])
def test_get_armor_z(direction, armor, compartment_name, part_name, val):
    assert SpaceShip.get_armor_z(direction, armor, compartment_name, part_name) == val


@pytest.mark.parametrize('length', [
    300,
    500,
    200,
])
def test_create_ship_parts(length):
    ship_part_length = int(length/paras.PART_SIZE)
    ship_parts = SpaceShip.create_ship_parts(length)
    ship_parts_keys = ship_parts.keys()
    assert len(ship_parts_keys) == ship_part_length + 2
    assert {0, 1, ship_part_length, ship_part_length + 1}.issubset(ship_parts_keys)
    assert ship_parts[0]['name'] == 'bow_shield'
    assert ship_parts[1]['name'] == 'bow'
    assert ship_parts[max(ship_parts_keys)]['name'] == 'stern_shield'
    assert ship_parts[max(ship_parts_keys) - 1]['name'] == 'stern'


@pytest.mark.parametrize('length', [
    100,
    0
])
def test_create_ship_parts_bad(length):
    with pytest.raises(ValueError):
        SpaceShip.create_ship_parts(length)


@pytest.mark.parametrize('name', [
    'asd',
    '',
    None
])
def test_get_compartments_dict(name):
    assert get_compartments_dict(name) == {'name': name,
                                           'compartments': {'shield_left': None,
                                                            'hull_left': None,
                                                            'middle': None,
                                                            'hull_right': None,
                                                            'shield_right': None
                                                            }}


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
    assert SpaceShip.get_surplus_weapons_array(weapons_cnt, cnt_broadside_parts) == (cnt_weapons_part, surplus_arr)
