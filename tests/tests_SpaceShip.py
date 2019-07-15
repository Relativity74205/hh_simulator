import pytest

from SpaceShip import SpaceShip, get_compartments_dict


def test_space_ship():
    pass


def test_add_weapons():
    pass


def test_create_compartments():
    pass


def test_get_compartment_health():
    pass


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


def test_get_shield_z():
    pass


def test_get_armor_x():
    pass


def test_get_armor_y():
    pass


def test_get_armor_z():
    pass


def test_create_ship_parts():
    pass


def test_init_parameters():
    pass


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
