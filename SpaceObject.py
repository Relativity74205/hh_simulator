from typing import Dict

import numpy as np

import vector_functions as vf
import global_parameters as paras


class SpaceObject:
    def __init__(self, name: str, size: np.array, mass: int, max_values: Dict[str, float],
                 position: np.array = np.array([0, 0, 0]),
                 velocity_val: float = 0,
                 velocity_vec: np.array = np.array([0, 0, 0]),
                 acceleration_val: float = 0,
                 acceleration_vec: np.array = np.array([0, 0, 0])):
        self.name = name
        self.size = size
        self.mass = mass
        self.position = position
        # TODO own function (val * vec)
        self.velocity = velocity_val * velocity_vec
        self.acceleration = acceleration_val * acceleration_vec
        self.max_velocity = max_values['velocity']
        self.max_acceleration = max_values['acceleration']

    def set_acceleration(self, acceleration, vec):
        unit_vec = vf.get_unit_vector(vec)
        if acceleration > self.max_acceleration:
            # TODO consequences
            acceleration = self.max_acceleration

        self.acceleration = acceleration * unit_vec

    def move(self):
        self.position += self.velocity * paras.TIMEDELTA_MOVE + 0.5 * self.acceleration * paras.TIMEDELTA_MOVE ** 2
        self.velocity += self.acceleration * paras.TIMEDELTA_MOVE
