"""Hero Script"""

# pylint: disable=missing-class-docstring

from ..entities import Character, Entity
from ..types import number  # pylint: disable=no-name-in-module
from ..enums import StateEnum
from ..basic_graphics import log_action, COMMON_ACTION_DEST


# Player character class
class Hero(Character):
    def __init__(
        self,
        name: str,
        hp: number,
        atk: number,
        defense: number,
        spd: number,
        mp: number,
    ):
        super().__init__(name, hp, atk, defense, spd, mp)
        self.max_mp = mp
        self.mp = mp
        self.max_energy = 150
        self.energy = 0
        self.crit_rate = 1
        self.crit_dmg = 55.2
        self.skill_mpcost = 20
        self.ult_encost = self.max_energy

    def basic_attack(self, target: Entity):
        self.generic_regen("energy", raw=10)
        self.generic_regen("mp", raw=20)
        log_action(f"[{self.name}] Invoke: Slash!", COMMON_ACTION_DEST)
        self.heal(0.1 * self.atk + 0.1 * self.max_hp)
        self.shield += 0.4 * self.atk + 0.05 * self.max_hp

        mult = self.impose_crit(10 * self.max_hp)
        return target.take_damage(mult)

    def skill(self, target: Entity):
        if self.mp < self.skill_mpcost:
            return StateEnum.NOT_ENOUGH_MP
        self.mp -= self.skill_mpcost
        self.generic_regen("energy", raw=15)

        log_action(f"[{self.name}] Invoke: Harder Slash!", COMMON_ACTION_DEST)
        # self.heal(0.04 * self.atk)
        # self.shield += 0.2 * self.atk
        if self.hp <= (self.max_hp * 0.75) and self.shield:
            burned_shield = self.shield * 0.5
            self.heal(burned_shield)
            self.shield -= burned_shield
        mult = self.impose_crit(20 * self.max_hp)
        return target.take_damage(mult)

    def ultimate(self, target: Entity):
        if self.energy < self.max_energy:
            return StateEnum.NOT_ENOUGH_MP
        self.energy = 0
        log_action(f'[{self.name}] Invoke: "Take This!"', COMMON_ACTION_DEST)
        burned_hp = self.hp * 0.75
        self.burn(burned_hp)
        self.shield += burned_hp * 0.5
        # if self.shield:
            # self.shield = self.max_hp * 0.25
        with self.temp("crit_dmg", 142.1):
            mult = self.impose_crit(120 * self.max_hp)
        self.generic_regen("mp", raw=100)
        return target.take_damage(mult)
