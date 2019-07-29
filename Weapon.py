from dataclasses import dataclass, field
from typing import List

from space_objects import weapon_systems
from Rocket import Rocket


@dataclass
class WeaponSystem:
    orientation: str
    type: str
    name: str
    cycle_time: float
    count: int = 0


@dataclass
class BeamWeapon(WeaponSystem):
    damage: float = 0


@dataclass
class RocketLauncher(WeaponSystem):
    ordnance: Rocket = None
    ordnance_count: int = None

    def add_ordnance(self, ordnance_name: str, ordnance_count):
        self.ordnance_count = ordnance_count
        self.ordnance = Rocket(ordnance_name)


@dataclass
class ShipWeapons:
    weapon_systems: List = field(default_factory=list, init=False)

    def add_weapon_system(self, weapon: WeaponSystem):
        self.weapon_systems.append(weapon)


def create_weapon_system(weapon_system_name: str, orientation: str) -> WeaponSystem:
    try:
        weapon_system_dict = weapon_systems[weapon_system_name]
    except KeyError:
        raise KeyError('Weapon system not found')

    if weapon_system_dict['type'] == 'beam':
        weapon = BeamWeapon(orientation, **weapon_system_dict)
    elif weapon_system_dict['type'] == 'rocket_launcher':
        weapon = RocketLauncher(orientation, **weapon_system_dict)
    else:
        raise KeyError('Weapon system type not valid')

    return weapon
