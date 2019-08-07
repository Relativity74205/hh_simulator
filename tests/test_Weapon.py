from unittest import mock

import pytest

import Weapon
import space_objects


@pytest.fixture
def weapon_dict():
    weapon_system_name = 'test'
    weapon_dict = space_objects.weapon_systems[weapon_system_name].copy()
    weapon_dict['name'] = weapon_system_name
    weapon_dict['orientation'] = 'bow'
    assert 'name' not in space_objects.weapon_systems[weapon_system_name].keys()
    assert 'orientation' not in space_objects.weapon_systems[weapon_system_name].keys()

    return weapon_dict


@pytest.fixture
def weapon_dict_beam():
    weapon_system_name = 'test_beam'
    weapon_dict_beam = space_objects.weapon_systems[weapon_system_name].copy()
    weapon_dict_beam['name'] = weapon_system_name
    weapon_dict_beam['orientation'] = 'bow'
    assert 'name' not in space_objects.weapon_systems[weapon_system_name].keys()
    assert 'orientation' not in space_objects.weapon_systems[weapon_system_name].keys()

    return weapon_dict_beam


def test_weaponsystem(weapon_dict):
    weapon = Weapon.WeaponSystem(**weapon_dict)
    assert weapon.orientation == 'bow'
    assert weapon.type == 'test'
    assert weapon.subtype == 'test_subtype'
    assert weapon.name == 'test'
    assert weapon.cycle_time == 42
    assert weapon.count == 0


def test_weaponsystem_count(weapon_dict):
    w = weapon_dict.copy()
    w['count'] = 3
    weapon = Weapon.WeaponSystem(**w)
    assert weapon.count == 3


def test_beamweapon(weapon_dict_beam):
    w = weapon_dict_beam.copy()
    weapon = Weapon.BeamWeapon(**w)
    assert weapon.damage == 42.42


def test_rocketlauncher(weapon_dict):
    weapon = Weapon.RocketLauncher(**weapon_dict)

    assert weapon.ordnance_count == 0
    assert not weapon.ordnance


def test_rocketlauncher_rocket(weapon_dict):
    w = weapon_dict.copy()
    with mock.patch('Rocket.Rocket') as rocket:
        w['ordnance'] = rocket
        w['ordnance_count'] = 4
        weapon = Weapon.RocketLauncher(**w)

        assert weapon.ordnance_count == 4
        assert weapon.ordnance == rocket


def test_shipweapons():
    shipweapons = Weapon.ShipWeapons()

    assert isinstance(shipweapons.weapon_systems, list)
    assert len(shipweapons.weapon_systems) == 0


def test_shipweapons_add_weapon_system(weapon_dict):
    weapon = Weapon.WeaponSystem(**weapon_dict)
    shipweapons = Weapon.ShipWeapons()
    shipweapons.add_weapon_system(weapon)

    assert shipweapons.weapon_systems[0] == weapon


def test_shipweapons_add_weapon_system_bad():
    shipweapons = Weapon.ShipWeapons()
    with pytest.raises(TypeError):
        shipweapons.add_weapon_system(1)


def test_create_weapon_system():
    weapon_system_name = 'test_beam'
    orientation = 'bow'

    weapon = Weapon.create_weapon_system(weapon_system_name, orientation)

    assert isinstance(weapon, Weapon.WeaponSystem)
    assert weapon.name == weapon_system_name
    assert weapon.orientation == 'bow'
    assert 'name' not in space_objects.weapon_systems[weapon_system_name].keys()


@pytest.mark.parametrize('weapon_system_name', [
    'asd',
    'test'
])
def test_create_weapon_system_bad_name(weapon_system_name):
    orientation = 'bow'

    with pytest.raises(KeyError):
        _ = Weapon.create_weapon_system(weapon_system_name, orientation)
