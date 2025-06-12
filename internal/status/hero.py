"""Hero's Buff"""
# pylint: disable=all

from typing import TYPE_CHECKING

from ..status_effect import StatusEffect, buff

if TYPE_CHECKING:
    from internal.entities import Entity
@buff
class ImpromptuEffect(StatusEffect):
    DESCRIPTION = "Increases Max HP by 120%, stackable for 2 stacks"

    def __init__(self, name: str, duration: int, max_stacks = 2):
        super().__init__(name, duration, max_stacks)
        self._bonus_applied = 0
        self._bonus_additive_applied = 0
        self.hp_bonus_percent_per_stack = 0.3  # 30%

    def apply(self, target: "Entity"):
        super().apply(target)
        self.remove(target)
        bonus = self.hp_bonus_percent_per_stack * self.stacks
        self._bonus_additive_applied = target.max_hp * bonus - target.max_hp
        target.stats.hp.multiplier += bonus
        target.hp += self._bonus_additive_applied  # Heal by bonus to avoid underflow
        self._bonus_applied = bonus
        print(f"{target.name}'s Max HP increased by {bonus} ({self.stacks} stacks).")

    def remove(self, target: "Entity"):
        target.stats.hp.multiplier -= self._bonus_applied
        target.hp -= self._bonus_additive_applied
        print(f"{target.name}'s Max HP boost wore off ({self._bonus_applied} removed, up to {self._bonus_additive_applied}).")
