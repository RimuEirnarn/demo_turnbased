"""Hero Script"""

# pylint: disable=missing-class-docstring

from internal.attributes import Attribute
from internal.elements import Elements
from ..entities import Character, Entity
from ..enums import StateEnum
from ..basic_graphics import log_action, COMMON_ACTION_DEST


# Player character class
class Hero(Character):
    def __init__(self, name: str, stats: Attribute):
        super().__init__(name, stats)
        self.max_energy = 110
        self.crit_rate = 1
        self.crit_dmg = 55.2
        self.skill_mpcost = 20
        self.ult_encost = self.max_energy
        self.element = Elements.RADIANCE

    def basic_attack(self, target: Entity):
        self.generic_regen("energy", raw=15)
        self.generic_regen("mp", raw=20)
        log_action(f"[{self.name}] Invoke: Slash!", COMMON_ACTION_DEST)
        self.heal(0.1 * self.atk + 0.1 * self.max_hp)
        self.shield += 0.4 * self.atk + 0.25 * self.max_hp

        mult = self.impose_crit(10 * self.max_hp)
        return target.take_damage(mult)

    def skill(self, target: Entity):
        if self.mp < self.skill_mpcost:
            return StateEnum.NOT_ENOUGH_MP
        self.mp -= self.skill_mpcost
        self.generic_regen("energy", raw=25)

        log_action(f"[{self.name}] Invoke: Harder Slash!", COMMON_ACTION_DEST)
        # self.heal(0.04 * self.atk)
        # self.shield += 0.2 * self.atk
        if self.hp <= (self.max_hp * 0.75) and self.shield:
            burned_shield = self.shield * 0.5
            self.heal(burned_shield + self.max_hp * 0.2)
            self.shield -= burned_shield
        elif self.shield < (self.max_hp * 0.5):
            self.shield += self.max_hp * 0.25
        mult = self.impose_crit(20 * self.max_hp)
        return target.take_damage(mult)

    def ultimate(self, target: Entity):
        if self.energy < self.max_energy:
            return StateEnum.NOT_ENOUGH_MP
        self.energy = 0
        log_action(f'[{self.name}] Invoke: "Take This!"', COMMON_ACTION_DEST)
        burned_hp = self.hp * 0.75
        self.burn(burned_hp)
        # self.shield += burned_hp * 0.4
        # if self.shield:
        # self.shield = self.max_hp * 0.25
        with self.temp("crit_dmg", 142.1 + self.crit_dmg):
            mult = self.impose_crit(120 * self.max_hp)
        self.generic_regen("mp", mult=0.5)
        return target.take_damage(mult)
