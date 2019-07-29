from typing import Dict, List
import math

import numpy as np

from SpaceObject import SpaceObject
from space_objects import ships
from Weapon import ShipWeapons, create_weapon_system, WeaponSystem
import global_parameters as paras

from Compartments import Compartment


class SpaceShip(SpaceObject):
    def __init__(self, ship_class_name: str):
        try:
            ship_class_dict = ships[ship_class_name]
        except KeyError:
            print(f'No ship with name {ship_class_name} in dict defined.')
            raise

        values_max = ship_class_dict['max_values']
        mass = ship_class_dict['mass']
        size = ship_class_dict['size']

        super().__init__(ship_class_name, size, mass, values_max)
        self.armor_dict = ship_class_dict['armor']
        self.shields_dict = ship_class_dict['shields']
        self.weapons_dict = ship_class_dict['weapons']
        self.orientation = None
        self.orientation_velocity = None
        self.orientation_acceleration = None
        self.rotation = None
        self.rotation_velocity = None
        self.rotation_acceleration = None
        self.weapons = ShipWeapons()
        self.compartments = []
        self.compartment_health_max = ship_class_dict['compartment_health']
        self.ship_length = get_ship_length(self.size)

        self.create_compartments()
        self.add_weapons()

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

    def create_compartments(self):
        if self.ship_length <= 1:
            raise ValueError(f'ship_length of {self.ship_length} too small')
        ship_parts = ['bow'] + [f'center_{i}' for i in range(1, self.ship_length - 1)] + ['stern']

        for pos_y, ship_part_x in enumerate(ship_parts):
            for pos_x, ship_part_y in enumerate(['hull_left', 'center', 'hull_right'], -1):
                compartment_name = f'{ship_part_x}-{ship_part_y}'
                compartment_armor = self.create_compartment_defense(self.armor_dict, ship_part_x, ship_part_y)
                compartment_shield = self.create_compartment_defense(self.shields_dict, ship_part_x, ship_part_y)
                compartment_health = self.compartment_health_max

                compartment = Compartment(compartment_name, pos_x, pos_y, compartment_health,
                                          compartment_armor, compartment_shield)
                self.compartments.append(compartment)

    def add_weapons(self):
        cnt_broadside_parts = get_cnt_broadside_parts(self.ship_length)
        broadside_indices = list(range(cnt_broadside_parts))
        for orientation in ['left', 'right', 'bow', 'stern']:
            weapon_systems: List = get_weapon_systems(orientation, self.weapons_dict)

            for weapon_system in weapon_systems:
                weapon_system_cnt = weapon_system['amount']
                weapon_system_name = weapon_system['name']
                cnt_weapons_part, surplus_weapons_index = \
                    self.get_surplus_weapons_array(weapon_system_cnt, cnt_broadside_parts)

                for broadside_index in broadside_indices:
                    for _ in range(cnt_weapons_part + broadside_index in surplus_weapons_index):
                        self.create_weapon(weapon_system_name, orientation, broadside_index)

    def create_weapon(self, weapon_system_name: str, orientation: str, broadside_index: int):
        weapon_system = create_weapon_system(weapon_system_name, orientation)
        self.weapons.add_weapon_system(weapon_system)
        self._add_weapon_to_compartment(weapon_system, orientation, broadside_index)

    def _add_weapon_to_compartment(self, weapon: WeaponSystem, orientation: str, pos_y: int):
        for compartment in self.compartments:
            if compartment.pos_y == pos_y and orientation in compartment.ship_part_x:
                compartment.add_component(weapon)
                break

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

    @staticmethod
    def create_compartment_defense(defense_dict: Dict, ship_part_x: str, ship_part_y: str) -> Dict[str, float]:
        directions = ['left', 'right', 'bow', 'stern', 'top', 'bottom']
        compartment_defense = {direction: get_defense_val(direction, defense_dict, ship_part_x, ship_part_y)
                             for direction in directions}

        return compartment_defense


def get_defense_val(direction: str, defense_dict: Dict, ship_part_x: str, ship_part_y: str) -> float:
    if direction in ['left', 'right']:
        if direction in ship_part_x:
            defense_val = defense_dict.get('broadside', 0)
        else:
            defense_val = defense_dict.get('inner', 0)
    elif direction in ['bow', 'stern']:
        if direction in ship_part_y:
            defense_val = defense_dict.get(direction, 0)
        else:
            defense_val = defense_dict.get('inner', 0)
    elif direction in ['top', 'bottom']:
        defense_val = defense_dict.get('vertical', 0)
    else:
        # TODO
        raise ValueError

    return defense_val


def get_ship_length(size: Dict[str, int]) -> int:
    return int(size['length'] / paras.PART_SIZE)


def get_cnt_broadside_parts(ship_length: int) -> int:
    return ship_length - 2


def get_weapon_systems(orientation: str, weapons_dict: Dict[str, List]) -> List:
    if orientation in ['left', 'right']:
        weapon_systems = weapons_dict['broadside']
    else:
        weapon_systems = weapons_dict[orientation]

    return weapon_systems
