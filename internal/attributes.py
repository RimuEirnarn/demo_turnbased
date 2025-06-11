"""Attributes"""

from dataclasses import dataclass, field
from math import ceil

from internal.elements import Elements
from internal.types import number

# pylint: disable=all

DEFAULT_MAPPING = {
    Elements.RADIANCE: 0,
    Elements.ABYSS: 0,
    Elements.PYRO: 0,
    Elements.HYDRO: 0,
    Elements.AERO: 0,
    Elements.ELECTRO: 0,
    Elements.GLACIO: 0,
    Elements.GEO: 0,
    Elements.PLANTEA: 0,
}

@dataclass
class Stat:
    base: float = 0
    multiplier: float = 0
    additive: int = 0

    @property
    def value(self):
        """Calculated value"""
        return self.base * (1 + self.multiplier) + self.additive

    def __int__(self):
        return ceil(self.value)

    def __float__(self):
        return self.value

    def __repr__(self):
        return f"<Stat base={self.base} mult={1+self.multiplier}% add={self.additive}>"

    def __add__(self, other: float) -> float:
        return float(self) + other

    def __sub__(self, other: float) -> float:
        return float(self) - other

    def __mul__(self, other: float) -> float:
        return float(self) * other

    def __div__(self, other: float) -> float:
        return float(self) / other


@dataclass
class EntityAttribute:
    hp: Stat
    atk: Stat
    def_: Stat
    spd: Stat

    effect_rate: number = 0
    effect_res: number = 0

    res: dict[Elements, number] = field(default_factory=DEFAULT_MAPPING.copy) # type: ignore
    res_pen: dict[Elements, number] = field(default_factory=DEFAULT_MAPPING.copy) # type: ignore
    bonus: dict[Elements, number] = field(default_factory=DEFAULT_MAPPING.copy) # type: ignore


@dataclass
class Attribute(EntityAttribute):
    crit_rate: number = 0.05
    crit_dmg: number = 0.5
