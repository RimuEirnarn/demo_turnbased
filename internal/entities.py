"""Entities"""
# pylint: disable=unused-argument,missing-class-docstring,missing-function-docstring

import random
from typing import Literal
from .enums import State
from .types import number
from .utils import Temporary
from .basic_graphics import log_action

class Entity:
    def __init__(
        self, name: str, hp: number, atk: number, defense: number, spd: number
    ):
        self.name = name
        self.max_hp = hp
        self.hp = hp
        self.atk = atk
        self.defense = defense
        self.spd = spd
        self.shield = 0

    def is_alive(self):
        return self.hp > 0

    def take_damage(self, dmg: number):
        actual_dmg = max(0, dmg - self.defense)
        if not self.shield:
            self.hp = max(0, self.hp - actual_dmg)
            return actual_dmg

        self.shield = self.shield - actual_dmg
        if self.shield < 0:
            self.hp = max(0, self.hp - abs(self.shield))
        return actual_dmg

    def attack(self, target: "Entity"):
        return target.take_damage(self.atk)

    def heal(self, value: number):
        self.hp = min(self.hp + value, self.max_hp)

    def temp(self, attr: str, value: number):
        return Temporary(self, attr, value)


# Player character class
class Character(Entity):
    def __init__(
        self,
        name: str,
        hp: number,
        atk: number,
        defense: number,
        spd: number,
        mp: number,
    ):
        super().__init__(name, hp, atk, defense, spd)
        self.max_mp = mp
        self.mp = mp
        self.max_energy = State.UNDEFINED
        self.energy = 0
        self.crit_rate = 0.25
        self.crit_dmg = 0.5
        self.skill_mpcost = State.UNDEFINED
        self.ult_encost = self.max_energy

    def check_mp(self, cost: number):
        return self.mp >= cost

    def check_energy(self, cost: number):
        return self.energy >= cost

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
                if self.max_energy == State.UNDEFINED:
                    raise ValueError("Cannot proceed with undefined Energy.")
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
        return State.UNDEFINED

    def skill(self, target: Entity):
        return State.UNDEFINED

    def ultimate(self, target: Entity):
        return State.UNDEFINED

    def impose_crit(self, base_dmg: number):
        if random.random() <= self.crit_rate:
            crit = base_dmg * (1 + self.crit_dmg)
            log_action(
                f"Does CRIT! from {round(base_dmg):,} to {round(crit):,} ({self.crit_dmg*100:,.2f}%)",
                (270, 75),
            )
            return crit
        return base_dmg


# Enemy class (inherits from Entity directly)
class Enemy(Entity):
    pass
