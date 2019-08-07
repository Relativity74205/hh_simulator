from unittest import mock

import pytest

import Compartments


defense_dict_1 = {'top': 1.0,
                  'bottom': 2.0,
                  'left': 3.0,
                  'right': 4.0,
                  'bow': 5.0,
                  'stern': 6.0}
defense_dict_2 = {'top': 11.0,
                  'bottom': 12.0,
                  'left': 13.0,
                  'right': 14.0,
                  'bow': 15.0,
                  'stern': 16.0}
compartment_name = 'x-y'


@pytest.fixture
def compartment():
    compartment = Compartments.Compartment(name=compartment_name,
                                           pos_x=1,
                                           pos_y=2,
                                           compartment_health=0.1,
                                           armor_dict=defense_dict_1,
                                           shield_dict=defense_dict_2
                                           )

    return compartment


def test_defense_default():
    defense = Compartments.Defense()

    assert defense.top == 0.0
    assert defense.bottom == 0.0
    assert defense.left == 0.0
    assert defense.right == 0.0
    assert defense.bow == 0.0
    assert defense.stern == 0.0


def test_defense():
    defense = Compartments.Defense(**defense_dict_1)

    assert defense.top == 1.0
    assert defense.bottom == 2.0
    assert defense.left == 3.0
    assert defense.right == 4.0
    assert defense.bow == 5.0
    assert defense.stern == 6.0


def test_armor():
    armor = Compartments.Armor()

    assert armor.top == 0.0
    assert armor.bottom == 0.0
    assert armor.left == 0.0
    assert armor.right == 0.0
    assert armor.bow == 0.0
    assert armor.stern == 0.0


def test_shield():
    shield = Compartments.Shield()

    assert shield.top == 0.0
    assert shield.bottom == 0.0
    assert shield.left == 0.0
    assert shield.right == 0.0
    assert shield.bow == 0.0
    assert shield.stern == 0.0
    assert shield.recharge_rate == 0.0


def test_compartment(compartment):
    assert compartment.name == compartment_name
    assert compartment.ship_part_x == 'x'
    assert compartment.ship_part_y == 'y'
    assert compartment.pos_x == 1
    assert compartment.pos_y == 2
    assert compartment.compartment_health == 0.1
    assert isinstance(compartment.armor, Compartments.Armor)
    assert compartment.armor.bottom == defense_dict_1['bottom']
    assert isinstance(compartment.shield, Compartments.Shield)
    assert compartment.shield.bottom == defense_dict_2['bottom']
    assert isinstance(compartment.shield_max, Compartments.Shield)
    assert compartment.shield_max.bottom == defense_dict_2['bottom']
    assert isinstance(compartment.components, list)
    assert len(compartment.components) == 0


def test_compartment_add_component(compartment):
    m = mock.Mock()
    compartment.add_component(m)

    assert len(compartment.components) == 1
    assert compartment.components[0] == m
