from typing import Dict, List
from dataclasses import dataclass


@dataclass
class Defense:
    top: float = 0.0
    bottom: float = 0.0
    left: float = 0.0
    right: float = 0.0
    bow: float = 0.0
    stern: float = 0.0


@dataclass
class Armor(Defense):
    pass


@dataclass
class Shield(Defense):
    recharge_rate: float = 0.0


class Compartment:
    def __init__(self, name: str, pos_x: int, pos_y: int, compartment_health: float,
                 armor_dict: Dict, shield_dict: Dict):
        self.name: str = name
        self.ship_part_x: str = name.split('-')[0]
        self.ship_part_y: str = name.split('-')[1]
        self.pos_x: int = pos_x
        self.pos_y: int = pos_y
        self.compartment_health: float = compartment_health
        self.armor: Armor = Armor(**armor_dict)
        self.shield: Shield = Shield(**shield_dict)
        self.shield_max: Shield = Shield(**shield_dict)
        self.components: List = []

    def add_component(self, component: any):
        self.components.append(component)
