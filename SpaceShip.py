from typing import Dict, List
import math

import numpy as np

from SpaceObject import SpaceObject
from space_objects import ships
from Weapon import BeamWeapon
import global_parameters as paras

from Compartments import Compartment


class SpaceShip(SpaceObject):
    def __init__(self, ship_class_name: str):
        try:
            ship_class_dict = ships[ship_class_name]
        except KeyError:
            print(f'No ship with name {ship_class_name} in dict defined.')
            raise

        max_values = ship_class_dict['max_values']
        mass = ship_class_dict['mass']
        size = ship_class_dict['size']

        super().__init__(ship_class_name, size, mass, max_values)
        self.max_orientation_velocity = max_values['orientation_velocity']
        self.max_orientation_acceleration = max_values['orientation_acceleration']
        self.max_rotation_velocity = max_values['rotation_velocity']
        self.max_rotation_acceleration = max_values['rotation_acceleration']
        self.orientation = None
        self.orientation_velocity = None
        self.orientation_acceleration = None
        self.rotation = None
        self.rotation_velocity = None
        self.rotation_acceleration = None
        self.weapons = {'stern': {},
                        'aft': {},
                        'left': {},
                        'right': {}}
        self.max_compartment_health = ship_class_dict['compartment_health']
        self.ship_parts, self.cnt_broadside_parts = self.create_ship_parts(size['length'])
        self.create_compartments(self.ship_parts,
                                 ship_class_dict['armor'], ship_class_dict['shields'],
                                 self.max_compartment_health)
        self.add_weapons(ship_class_dict['weapons'])

    def add_weapons(self, weapons_dict: Dict):
        weapons_broadside = weapons_dict['broadside']
        weapons_stern = weapons_dict['stern']
        weapons_aft = weapons_dict['aft']

        inner_ship_part_keys = [key for key in self.ship_parts.keys() if 'inner' in self.ship_parts[key]['name']]
        for weapon in weapons_broadside:
            weapon_cnt = weapon['amount']
            weapon_name = weapon['name']
            cnt_weapons_part, surplus_weapons_index = \
                self.get_surplus_weapons_array(weapon_cnt, self.cnt_broadside_parts)

            for key in inner_ship_part_keys:
                inner_ship_part_index = int(self.ship_parts[key]['name'].split('_')[1]) - 1
                if inner_ship_part_index in surplus_weapons_index:
                    weapon_cnt += 1
                self.add_weapon_to_compartment(weapon_name, weapon_cnt, key)

    def add_weapon_to_compartment(self, weapon_name: str, weapon_cnt: int, inner_ship_part_key: int):
        weapon = BeamWeapon()
        if weapon_name in self.weapons['left']:
            self.weapons['left'][weapon_name] += weapon_cnt
        else:
            self.weapons['left'][weapon_name] = weapon_cnt
        if weapon_name in self.weapons['left']:
            self.weapons['right'][weapon_name] += weapon_cnt
        else:
            self.weapons['right'][weapon_name] = weapon_cnt

        self.ship_parts[inner_ship_part_key]

    @staticmethod
    def get_surplus_weapons_array(weapon_cnt: int, cnt_broadside_parts: int) -> (int, List[int]):
        if cnt_broadside_parts == 0:
            cnt_weapons_part = 0
            surplus_weapons_index = []
        else:
            cnt_weapons_part = int(weapon_cnt / cnt_broadside_parts)
            surplus_weapons = weapon_cnt - cnt_weapons_part * cnt_broadside_parts
            surplus_weapons_index = [math.floor((i + 0.5) * (cnt_broadside_parts - 1) / surplus_weapons)
                                     if (i + 0.5) * (cnt_broadside_parts - 1) / surplus_weapons < cnt_broadside_parts / 2
                                     else math.ceil((i + 0.5) * (cnt_broadside_parts - 1) / surplus_weapons)
                                     for i in range(surplus_weapons)]

        return cnt_weapons_part, surplus_weapons_index

    def create_compartments(self, ship_parts: Dict, armor_dict: Dict, shields_dict: Dict, max_compartment_health: float):
        for _, ship_part in ship_parts.items():
            ship_part_name = ship_part['name']
            compartments = ship_part['compartments']
            for compartment_name in compartments.keys():
                compartment_health = self.get_compartment_health(compartment_name,
                                                                 ship_part_name,
                                                                 max_compartment_health)

                compartment_shield = dict()
                compartment_shield['left'] = self.get_shield_x('left', shields_dict, compartment_name)
                compartment_shield['right'] = self.get_shield_x('right', shields_dict, compartment_name)
                compartment_shield['bow'] = self.get_shield_y('bow', shields_dict, compartment_name)
                compartment_shield['stern'] = self.get_shield_y('stern', shields_dict, compartment_name)
                compartment_shield['top'] = self.get_shield_z('top', shields_dict)
                compartment_shield['bottom'] = self.get_shield_z('bottom', shields_dict)

                compartment_armor = dict()
                compartment_armor['left'] = self.get_armor_x('left', armor_dict, compartment_name, ship_part_name)
                compartment_armor['right'] = self.get_armor_x('right', armor_dict, compartment_name, ship_part_name)
                compartment_armor['bow'] = self.get_armor_y('bow', armor_dict, compartment_name, ship_part_name)
                compartment_armor['stern'] = self.get_armor_y('stern', armor_dict, compartment_name, ship_part_name)
                compartment_armor['top'] = self.get_armor_z('top', armor_dict, compartment_name, ship_part_name)
                compartment_armor['bottom'] = self.get_armor_z('bottom', armor_dict, compartment_name, ship_part_name)

                compartments[compartment_name] = Compartment('', compartment_health, compartment_armor, compartment_shield)

    @staticmethod
    def get_compartment_health(compartment_name: str, ship_part_name: str, health: float) -> float:
        if compartment_name.startswith('shield') or ship_part_name.endswith('shield'):
            compartment_health = 0
        else:
            compartment_health = health

        return compartment_health

    @staticmethod
    def get_shield_x(direction: str, shields_dict: Dict, compartment_name: str) -> float:
        if direction in compartment_name and 'shield' in compartment_name and direction in ['left', 'right']:
            shield = shields_dict.get('broadside', 0)
        else:
            shield = 0

        return shield

    @staticmethod
    def get_shield_y(direction: str, shields_dict: Dict, ship_part_name: str) -> float:
        if direction in ship_part_name and 'shield' in ship_part_name and direction in ['bow', 'stern']:
            shield = shields_dict.get(direction, 0)
        else:
            shield = 0

        return shield

    @staticmethod
    def get_shield_z(direction: str, shields_dict: Dict) -> float:
        if direction in ['top', 'bottom']:
            shield = shields_dict.get('vertical', 0)
        else:
            shield = 0

        return shield

    @staticmethod
    def get_armor_x(direction: str, armor_dict: Dict, compartment_name: str, ship_part_name: str) -> float:
        if 'shield' in ship_part_name or 'shield' in compartment_name:
            armor = 0
        else:
            if direction in compartment_name and direction in ['left', 'right']:
                armor = armor_dict.get('broadside', 0)
            else:
                armor = armor_dict.get('inner', 0)

        return armor

    @staticmethod
    def get_armor_y(direction: str, armor_dict: Dict, compartment_name: str, ship_part_name: str) -> float:
        if 'shield' in ship_part_name or 'shield' in compartment_name:
            armor = 0
        else:
            if direction in ship_part_name and direction in ['bow', 'stern']:
                armor = armor_dict.get(direction, 0)
            else:
                armor = armor_dict.get('inner', 0)

        return armor

    @staticmethod
    def get_armor_z(direction: str, armor_dict: Dict, compartment_name: str, ship_part_name: str) -> float:
        if 'shield' in ship_part_name or 'shield' in compartment_name:
            armor = 0
        else:
            if direction in ['top', 'bottom']:
                armor = armor_dict.get('vertical', 0)
            else:
                armor = 0

        return armor

    @staticmethod
    def create_ship_parts(length: int) -> (Dict[int, Dict], int):
        ship_part_length = int(length/paras.PART_SIZE)

        if ship_part_length > 1:
            ship_parts = {0: get_compartments_dict('bow_shield'),
                          1: get_compartments_dict('bow'),
                          ship_part_length: get_compartments_dict('stern'),
                          ship_part_length + 1: get_compartments_dict('stern_shield')
                          }

            cnt_broadside_parts = 0
            for i in range(2, ship_part_length):
                ship_parts[i] = get_compartments_dict(f'inner_{i}')
                cnt_broadside_parts += 1
        else:
            raise ValueError(f'ship_length of {length} too small')

        return ship_parts, cnt_broadside_parts

    def init_parameters(self,
                        orientation: np.array = np.array([0, 0, 0]),
                        orientation_velocity: np.array = np.array([0, 0, 0]),
                        orientation_acceleration: np.array = np.array([0, 0, 0]),
                        rotation: int = 0,
                        rotation_velocity: int = 0,
                        rotation_acceleration: int = 0):
        self.orientation = orientation
        self.orientation_velocity = orientation_velocity
        self.orientation_acceleration = orientation_acceleration
        self.rotation = rotation
        self.rotation_velocity = rotation_velocity
        self.rotation_acceleration = rotation_acceleration


def get_compartments_dict(name: str):
    return {'name': name,
            'compartments': {'shield_left': None,
                             'hull_left': None,
                             'middle': None,
                             'hull_right': None,
                             'shield_right': None
                             }
            }
