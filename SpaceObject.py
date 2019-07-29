from typing import Dict

import numpy as np

import vector_functions as vf
import global_parameters as paras


class SpaceObject:
    def __init__(self, name: str, size: np.array, mass: int, values_max: Dict[str, float],
                 position: np.array = np.array([0., 0., 0.]),
                 velocity_val: float = 0.,
                 velocity_vec: np.array = np.array([0., 0., 0.]),
                 acceleration_val: float = 0.,
                 acceleration_vec: np.array = np.array([0., 0., 0.])):
        self.name = name
        self.size = size
        self.mass = mass
        self.position = position
        self.velocity = None
        self.acceleration = None
        self.values_max = values_max

        self.set_velocity(velocity_val, velocity_vec)
        self.set_acceleration(acceleration_val, acceleration_vec)

    def set_velocity(self, v, v_vec):
        unit_vec = vf.get_unit_vector(v_vec)
        if v > self.values_max['velocity']:
            # TODO consequences
            v = self.values_max['velocity']

        self.velocity = unit_vec * v

    def set_acceleration(self, a, a_vec):
        unit_vec = vf.get_unit_vector(a_vec)
        if a > self.values_max['acceleration']:
            # TODO consequences
            a = self.values_max['acceleration']

        self.acceleration = unit_vec * a

    def move(self):
        self.position += self.velocity * paras.TIMEDELTA_MOVE + 0.5 * self.acceleration * paras.TIMEDELTA_MOVE ** 2
        self.velocity += self.acceleration * paras.TIMEDELTA_MOVE
