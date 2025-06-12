# pylint: disable=all

from enum import IntEnum
from typing import TYPE_CHECKING, Type, TypeVar

if TYPE_CHECKING:
    from .entities import Entity

TypeSE = TypeVar("TypeSE", bound="StatusEffect")

class EffectType(IntEnum):
    BUFF = 1
    NEUTRAL = 0
    DEBUFF = -1

class StatusEffect:
    def __init__(self, name: str, duration: int, max_stacks: int = 1):
        self.name = name
        self.duration = duration
        self.remaining_duration = duration
        self.stacks = 1
        self.max_stacks = max_stacks
        self.active = True
        self.type = EffectType.NEUTRAL

    def apply(self, target: "Entity"):
        """Apply effect logic. Override in subclass."""
        print(f"{self.name} applied to {target} for {self.remaining_duration} turn(s), {self.stacks} stack(s).")

    def remove(self, target: "Entity"):
        """Clean up the effect."""
        print(f"{self.name} removed from {target}.")

    def refresh_or_stack(self):
        """Called when the same effect is re-applied."""
        if self.stacks < self.max_stacks:
            self.stacks += 1
            print(f"{self.name} stack increased to {self.stacks}.")
        else:
            print(f"{self.name} already at max stacks ({self.max_stacks}).")
        self.remaining_duration = self.duration

    def on_turn_start(self, target: "Entity"):
        if not self.active:
            return

    def on_turn_end(self, target: "Entity"):
        if not self.active:
            return
        self.remaining_duration -= 1
        print(f"{self.name} ticking... ({self.remaining_duration} turns left)")
        if self.remaining_duration <= 0:
            self.active = False
            self.remove(target)

# === Decorators ===

def buff(cls: Type[TypeSE]):
    cls.type = EffectType.BUFF # type: ignore
    return cls

def debuff(cls: Type[TypeSE]):
    cls.type = EffectType.DEBUFF # type: ignore
    return cls

def neutral(cls: Type[TypeSE]):
    cls.type = EffectType.NEUTRAL # type: ignore
    return cls
