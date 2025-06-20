"""Enums"""
# pylint: disable=invalid-name

from enum import IntEnum

class StateEnum(IntEnum):
    """State result during incantation"""
    NOT_ENOUGH_MP = -1
    NOT_ENOUGH_ENERGY = -2
    UNDEFINED = -999
    OK = -1000

class Elements(IntEnum):
    """Elements"""

    Radiance = 1
    Abyss = 2
    Pyro = 3
    Hydro = 4
    Electro = 5
    Glacio = 6
    Aero = 7
    Geo = 8
    Plantea = 9

class EntityType(IntEnum):
    """Entity Type"""
    CHARACTERS = 1
    ENEMY = 0
    SUMMONS = 2
    ACTIONS = 3
    UNDEFINED = -1

class DamageType(IntEnum):
    """Damage types"""

    # HAS TO BE EQUAL
    Radiance = 1
    Abyss = 2
    Pyro = 3
    Hydro = 4
    Electro = 5
    Glacio = 6
    Aero = 7
    Geo = 8
    Plantea = 9

    TRUE = 0
    Base = -1

class ActionType(IntEnum):
    """Action Types"""
    NORMAL = 0
    FOLLOW_UP = 1
    ULTIMATE = 2
    EXTRA_ACTION = -1
