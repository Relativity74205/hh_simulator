from typing import Dict

import numpy as np

from SpaceObject import SpaceObject
from space_objects import ships
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
        self.compartment_health = ship_class_dict['compartment_health']
        self.ship_parts = self.create_ship_parts(size['length'])
        self.create_compartments(ship_class_dict['armor'], ship_class_dict['shields'])

        self.add_weapons(ship_class_dict['weapons'])

    def add_weapons(self, weapons_dict: Dict):
        pass

    def create_compartments(self, armor_dict: Dict, shields_dict: Dict):
        for _, ship_part in self.ship_parts.items():
            ship_part_name = ship_part['name']
            compartments = ship_part['compartments']
            for compartment_name in compartments.keys():
                compartment_health = self.get_compartment_health(compartment_name, ship_part_name,
                                                                 self.compartment_health)

                compartment_shield = dict()
                compartment_shield['left'] = self.get_shield_x('left', shields_dict, compartment_name)
                compartment_shield['right'] = self.get_shield_x('right', shields_dict, compartment_name)
                compartment_shield['bow'] = self.get_shield_y('bow', shields_dict, compartment_name)
                compartment_shield['stern'] = self.get_shield_y('stern', shields_dict, compartment_name)
                compartment_shield['top'] = self.get_shield_z(shields_dict)
                compartment_shield['bottom'] = self.get_shield_z(shields_dict)

                compartment_armor = dict()
                compartment_armor['left'] = self.get_armor_x('left', armor_dict, compartment_name, ship_part_name)
                compartment_armor['right'] = self.get_armor_x('right', armor_dict, compartment_name, ship_part_name)
                compartment_armor['bow'] = self.get_armor_y('bow', armor_dict, compartment_name, ship_part_name)
                compartment_armor['stern'] = self.get_armor_y('stern', armor_dict, compartment_name, ship_part_name)
                compartment_armor['top'] = self.get_armor_z(armor_dict, compartment_name, ship_part_name)
                compartment_armor['bottom'] = self.get_armor_z(armor_dict, compartment_name, ship_part_name)

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
        if direction in compartment_name and 'shield' in compartment_name:
            shield = shields_dict['broadside']
        else:
            shield = 0

        return shield

    @staticmethod
    def get_shield_y(direction: str, shields_dict: Dict, ship_part_name: str) -> float:
        if direction in ship_part_name and 'shield' in ship_part_name:
            shield = shields_dict[direction]
        else:
            shield = 0

        return shield

    @staticmethod
    def get_shield_z(shields_dict: Dict) -> float:
        shield = shields_dict['vertical']

        return shield

    @staticmethod
    def get_armor_x(direction: str, armor_dict: Dict, compartment_name: str, ship_part_name: str) -> float:
        if 'shield' in ship_part_name or 'shield' in compartment_name:
            armor = 0
        else:
            if direction in compartment_name:
                armor = armor_dict['broadside']
            else:
                armor = armor_dict['inner']

        return armor

    @staticmethod
    def get_armor_y(direction: str, armor_dict: Dict, compartment_name: str, ship_part_name: str) -> float:
        if 'shield' in ship_part_name or 'shield' in compartment_name:
            armor = 0
        else:
            if direction in ship_part_name:
                armor = armor_dict[direction]
            else:
                armor = armor_dict['inner']

        return armor

    @staticmethod
    def get_armor_z(armor_dict: Dict, compartment_name: str, ship_part_name: str) -> float:
        if 'shield' in ship_part_name or 'shield' in compartment_name:
            armor = 0
        else:
            armor = armor_dict['vertical']

        return armor

    @staticmethod
    def create_ship_parts(length: int) -> Dict[int, Dict]:
        ship_part_length = int(length/paras.PART_SIZE)
        ship_parts = {0: get_compartments_dict('bow_shield'),
                      1: get_compartments_dict('bow'),
                      ship_part_length: get_compartments_dict('stern'),
                      ship_part_length + 1: get_compartments_dict('stern_shield')
                      }
        for i in range(2, ship_part_length):
            ship_parts[i] = get_compartments_dict(f'inner_{i}')
        return ship_parts

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
