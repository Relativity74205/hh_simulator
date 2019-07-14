from typing import Dict


class Defense:
    def __init__(self, val_dict: Dict):
        self.top = self._get_value(val_dict, 'top')
        self.bottom = self._get_value(val_dict, 'bottom')
        self.left = self._get_value(val_dict, 'left')
        self.right = self._get_value(val_dict, 'right')
        self.bow = self._get_value(val_dict, 'bow')
        self.stern = self._get_value(val_dict, 'stern')

    @staticmethod
    def _get_value(d, key):
        return d.get(key, 0)


class Armor(Defense):
    def __init__(self, armor_dict: Dict):
        super().__init__(armor_dict)


class Shield(Defense):
    def __init__(self, shield_dict: Dict, recharge_rate: float = 0):
        super().__init__(shield_dict)
        self.shield_dict_max = shield_dict
        self.recharge_rate = recharge_rate


class Compartment:
    def __init__(self, name: str, compartment_health: float, armor_dict: Dict, shield_dict: Dict):
        self.name = name
        self.health = compartment_health
        self.armor = Armor(armor_dict)
        self.shield = Shield(shield_dict)
        self.components = []
