from typing import Dict

import numpy as np

from SpaceObject import SpaceObject
import vector_functions as vf
import global_parameters as paras


class Rocket(SpaceObject):
    def __init__(self, size: np.array, mass: int, max_values: Dict[str, float]):
        super().__init__(size, mass, max_values)
        pass


class BeamWeapon(SpaceObject):
    def __init__(self, name: str, damage: int, cycle_time: int,
                 position: np.array = np.array([0, 0, 0]),
                 velocity_vec: np.array = np.array([0, 0, 0])):
        max_values = {'velocity': 300000,
                      'acceleration': 0
                      }
        super().__init__(name=name, size=np.array([0, 0, 0]), mass=0, max_values=max_values,
                         position=position, velocity_val=paras.C, velocity_vec=velocity_vec)
        self.damage = damage
        self.cycle_time = cycle_time

