"""Healer"""

# pylint: disable=missing-class-docstring,missing-function-docstring,arguments-renamed

from typing import Iterable

from internal.enums import StateEnum
from ..entities import Character, Entity

class Healer(Character):
    def __init__(self, name, hp, atk, defense, spd, mp):
        super().__init__(name, hp, atk, defense, spd, mp)
        self.max_energy = 100
        self.skill_mpcost = 20
        self.crit_rate = 1
        self.crit_dmg = 1.5

    def basic_attack(self, target):
        damage = self.impose_crit(0.5 * self.max_hp)
        self.generic_regen('mp', 0.2)
        return target.take_damage(damage)

    def skill(self, targets: Iterable[Entity]):
        if not self.check_mp(self.max_mp * 0.2):
            return StateEnum.NOT_ENOUGH_MP
        self.mp -= self.skill_mpcost

        for target in targets:
            target.shield += self.max_hp * 0.45

        return StateEnum.OK

    def ultimate(self, targets: Iterable[Entity]):
        if not self.check_energy(self.max_energy):
            return StateEnum.NOT_ENOUGH_ENERGY
        self.energy -= self.max_energy

        for target in targets:
            target.shield += self.max_hp * 0.75
        return StateEnum.OK
