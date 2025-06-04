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
