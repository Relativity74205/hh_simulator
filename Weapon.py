from typing import Dict

import numpy as np

from SpaceObject import SpaceObject
from space_objects import weapon_systems, weapons
import global_parameters as paras


class ShipWeapons:
    def __init__(self):
        self.bow: WeaponCluster = WeaponCluster()
        self.stern: WeaponCluster = WeaponCluster()
        self.left: WeaponCluster = WeaponCluster()
        self.right: WeaponCluster = WeaponCluster()


class WeaponCluster:
    def __init__(self):
        self.beam_offensive = {}
        self.beam_defensive = {}
        self.missile_launcher = {}
        self.missile_defensive = {}
        self.energy_torpedos = {}

    def add_weapon(self, weapon_system_name: str, weapon_cnt: int):
        try:
            weapon_system = weapon_systems[weapon_system_name]
            weapon_type = weapon_system['type']
            weapon_type_dict: Dict = getattr(self, weapon_type)
            try:
                weapon_name = weapon_systems['weapon_name']
            except KeyError:
                weapon_name = weapon_system_name

            if weapon_system_name in weapon_type_dict.keys():
                weapon_type_dict[weapon_system_name] = WeaponSystem(weapon_system_name)
            else:
                weapon_type_dict[weapon_system_name]['count'] += weapon_cnt
        except KeyError:
            pass


class WeaponSystem:
    def __init__(self, weapon_system_name: str, weapon_cnt: int):
        self.count = weapon_cnt
        self.cycle_time = weapon_system['cycle_time']
        self.weapon = {'weapon_name': weapon_name,
                       'damage': '',
                       'max_velocity': 0,
                       'max_acceleration': 0}

        try:
            weapon_system = weapon_systems[weapon_system_name]
        except KeyError:
            print(f'No ship with name {weapon_system_name} in dict defined.')
            raise

        self.type = weapon_system['type']
        self.cycle_time = weapon_system['cycle_time']
        try:
            self.weapon_name = weapon_system['weapon_name']
        except KeyError:
            self.weapon_name = weapon_system_name


class Weapon(SpaceObject):
    def __init__(self, weapon_name: str,
                 position: np.array = np.array([0, 0, 0]),
                 velocity_vec: np.array = np.array([0, 0, 0])):
        try:
            weapon_dict = weapons[weapon_name]
        except KeyError:
            print(f'No ship with name {weapon_name} in dict defined.')
            raise

        self.type = weapon_dict['type']
        if self.type == 'beam':
            max_values = {'velocity': 300000,
                          'acceleration': 0
                          }
            mass = 0
            size = {'length': 0,
                    'height': 0,
                    'width': 0
                    }
        else:
            max_values = weapon_dict['max_values']
            mass = weapon_dict['mass']
            size = weapon_dict['size']

        super().__init__(name=weapon_name, size=size, mass=mass, max_values=max_values,
                         position=position, velocity_val=paras.C, velocity_vec=velocity_vec)
        self.damage = weapon_dict['damage']
