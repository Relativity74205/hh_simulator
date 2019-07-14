import numpy as np

import space_objects
import Weapon
import SpaceShip


name = 'LaserMkI'
w_dict = space_objects.weapons[name]
bw = Weapon.BeamWeapon(name, **w_dict, position=np.array([0, 0, 0]), velocity_vec=np.array([1, 0, 0]))

######

hms = SpaceShip.SpaceShip('Cruiser')

a = 1
