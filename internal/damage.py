"""Damage"""

# pylint: disable=missing-class-docstring,missing-function-docstring

from random import random
from typing import NamedTuple

from internal.enums import EntityType
from internal.types import number

# Constants

DEF_COEFFICIENT = 5000
ENEMY_DEF_COEFFICIENT = 2450


class CommonMultipliers(NamedTuple):
    elemental: number
    dmg_boost: number
    res_pen: number
    res_shred: number
    def_shred: number
    def_ignore: number


class DefenderMultipliers(NamedTuple):
    res: number


class CommonAttribute(NamedTuple):
    level: int
    def_: int
    type_: EntityType
    crit_rate: number = 0
    crit_dmg: number = 0


def impose_crit(rate: number, mult: number):
    return 1 + mult if random() < rate else 1


def damage_boost(mult: CommonMultipliers):
    return 1 + mult.elemental + mult.dmg_boost


def def_multiplier_character(def_: number):
    return 1 / (1 + def_ / DEF_COEFFICIENT)


def def_multiplier_enemy(attacker_mult: CommonMultipliers, defender: CommonAttribute):
    return 1 / (
        (
            1
            + (defender.def_ * (1 - attacker_mult.def_shred - attacker_mult.def_ignore))
            / ENEMY_DEF_COEFFICIENT
        )
    )


def res_mult(defender: DefenderMultipliers, attacker: CommonMultipliers):
    return 1 - (defender.res - attacker.res_pen - attacker.res_shred)


def calculate_hit(
    base_dmg,
    attacker: CommonAttribute,
    defender: CommonAttribute,
    attacker_mult: CommonMultipliers,
    defender_mult: DefenderMultipliers,
):
    return (
        base_dmg
        * impose_crit(attacker.crit_rate, attacker.crit_dmg)
        * damage_boost(attacker_mult)
        * (
            def_multiplier_enemy(attacker_mult, defender)
            if defender.type_ == EntityType.ENEMY
            else def_multiplier_character(defender.def_)
        )
        * res_mult(defender_mult, attacker_mult)
    )
