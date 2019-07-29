import numpy as np

from SpaceObject import SpaceObject
from space_objects import weapon_systems, ordnance, weapons


class Rocket(SpaceObject):
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