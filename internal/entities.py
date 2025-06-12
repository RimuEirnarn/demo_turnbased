"""Entities"""

# pylint: disable=unused-argument,missing-class-docstring,missing-function-docstring

import random
from typing import Literal

from internal.attributes import Attribute, EntityAttribute
from internal.elements import Elements

from .enums import EntityType, StateEnum
from .types import number
from .utils import Temporary
from .basic_graphics import log_action, COMMON_CRIT_DEST


class Entity:
    def __init__(self, name: str, stats: EntityAttribute):
        self.name = name
        self.stats = stats
        self.hp = self.max_hp
        self.shield = 0
        self.type = EntityType.UNDEFINED
        self.element = Elements.UNDEFINED

    @property
    def max_hp(self):
        """Max HP"""
        return self.stats.hp.value

    @property
    def atk(self):
        """ATK"""
        return self.stats.atk.value

    @property
    def defense(self):
        """DEF"""
        return self.stats.def_.value

    @property
    def spd(self):
        """SPD"""
        return self.stats.spd

    def is_alive(self):
        """Return true if HP is more than 0"""
        return self.hp > 0

    def take_damage(self, dmg: number):
        """This unit takes damage based on damage"""
        actual_dmg = max(0, dmg - self.defense)
        if not self.shield:
            self.hp = max(0, self.hp - actual_dmg)
            return actual_dmg

        self.shield = self.shield - actual_dmg
        if self.shield < 0:
            self.hp = max(0, self.hp - abs(self.shield))
            self.shield = 0
        return actual_dmg

    def attack(self, target: "Entity"):
        """Attack a target"""
        return target.take_damage(self.atk)

    def heal(self, value: number):
        """Heal this unit based on value"""
        self.hp = min(self.hp + value, self.max_hp)

    def temp(self, attr: str, value: number):
        """Temporarily change a value"""
        return Temporary(self, attr, value)


# Player character class
class Character(Entity):
    def __init__(self, name: str, stats: Attribute):
        super().__init__(name, stats)
        self.stats: Attribute = stats
        self.max_mp = self.stats.mp.value
        self.mp = self.max_mp
        self.max_energy = StateEnum.UNDEFINED
        self.energy = 0
        self.skill_mpcost = StateEnum.UNDEFINED
        self.ult_encost = self.max_energy
        self.type = EntityType.CHARACTERS

    @property
    def crit_rate(self):
        """Crit Rate"""
        return self.stats.crit_rate

    @crit_rate.setter
    def crit_rate(self, cr: number):
        """Crit Rate"""
        self.stats.crit_rate = cr

    @property
    def crit_dmg(self):
        """Crit DMG"""
        return self.stats.crit_dmg

    @crit_dmg.setter
    def crit_dmg(self, cdmg: number):
        """Crit DMG"""
        self.stats.crit_dmg = cdmg

    def check_mp(self, cost: number):
        """Check if current MP is more than cost"""
        return self.mp >= cost

    def check_energy(self, cost: number):
        """Check if current energy is more than cost"""
        return self.energy >= cost

    def burn(self, value: number):
        """Burn current HP based on value"""
        if 0 < value < 1:
            value = 1
        self.hp = max(min(self.hp, self.hp - value), 1)

    def generic_regen(self, type_: Literal["energy", "mp"], mult: number = -1, raw=-1):
        """Apply regeneration for MP/Energy based on multiplier or raw value"""
        if mult == -1 and raw == -1:
            print("Error: Either provide raw value or multiplier increase")
            return
        match type_:
            case "energy":
                if self.max_energy == StateEnum.UNDEFINED:
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
        """Deals basic attack"""
        return StateEnum.UNDEFINED

    def skill(self, target: Entity):
        """Deals Skill"""
        return StateEnum.UNDEFINED

    def ultimate(self, target: Entity):
        """Deals Ultimate"""
        return StateEnum.UNDEFINED

    def impose_crit(self, base_dmg: number):
        """Impose crit on this hit"""
        if random.random() <= self.crit_rate:
            crit = base_dmg * (1 + self.crit_dmg)
            log_action(
                f"Does CRIT! from {round(base_dmg):,} to {round(crit):,} ({self.crit_dmg*100:,.2f}%)",
                COMMON_CRIT_DEST,
            )
            return crit
        return base_dmg


# Enemy class (inherits from Entity directly)
class Enemy(Entity):
    def __init__(self, name: str, stats: EntityAttribute):
        super().__init__(name, stats)
        self.type = EntityType.ENEMY
