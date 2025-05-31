"""Hero Script"""
import random
from typing import Literal
from ..entities import Player, Entity
from ..types import number # pylint: disable=no-name-in-module
from ..enums import State
from ..basic_graphics import log_action

# Player character class
class Hero(Player):
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
        self.crit_rate = 0.75
        self.crit_dmg = 55.2
        self.skill_mpcost = 20
        self.ult_encost = self.max_energy

    def burn(self, value: number):
        if 0 < value < 1:
            value = 1
        self.hp = max(min(self.hp, self.hp - value), 1)

    def generic_regen(self, type_: Literal["energy", "mp"], mult: number = -1, raw=-1):
        if mult == -1 and raw == -1:
            print("Error: Either provide raw value or multiplier increase")
            return
        match type_:
            case "energy":
                if mult != -1:
                    base = self.max_energy * mult
                else:
                    base = raw
                self.energy = min(self.energy + base, self.max_energy)
                return
            case "mp":
                if mult != -1:
                    base = self.max_mp * mult
                else:
                    base = raw
                self.mp = min(self.mp + base, self.max_mp)
                return

    def basic_attack(self, target: Entity):
        self.generic_regen("energy", raw=10)
        self.generic_regen("mp", raw=20)
        log_action(f"[{self.name}] Invoke: Slash!", (270, 50))
        self.heal(0.4 * self.atk)
        mult = self.impose_crit(40 * self.atk)
        return target.take_damage(mult)

    def skill(self, target: Entity):
        if self.mp < self.skill_mpcost:
            return State.NOT_ENOUGH_MP
        self.mp -= self.skill_mpcost
        self.generic_regen("energy", raw=15)

        log_action(f"[{self.name}] Invoke: Harder Slash!", (270, 50))
        self.heal(0.4 * self.atk)
        mult = self.impose_crit(60 * self.atk)
        return target.take_damage(mult)

    def ultimate(self, target: Entity):
        if self.energy < self.max_energy:
            return State.NOT_ENOUGH_MP
        self.energy = 0
        log_action(f'[{self.name}] Invoke: "Take This!"', (270, 50))
        self.burn(self.hp * 0.8)
        with self.temp("crit_dmg", 142.1):
            mult = self.impose_crit(120 * self.atk)
        self.generic_regen("mp", raw=100)
        return target.take_damage(mult)

    def impose_crit(self, base_dmg: number):
        if random.random() <= self.crit_rate:
            crit = base_dmg * (1 + self.crit_dmg)
            log_action(
                f"Does CRIT! from {round(base_dmg):,} to {round(crit):,} ({self.crit_dmg*100:,.2f}%)",
                (270, 75),
            )
            return crit
        return base_dmg
