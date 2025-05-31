"""Enums"""

from enum import IntEnum

class State(IntEnum):
    """State result during incantation"""
    NOT_ENOUGH_MP = -1
    NOT_ENOUGH_ENERGY = -2
    UNDEFINED = -999
