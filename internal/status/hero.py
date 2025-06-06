"""Hero's Buff"""
# pylint: disable=all

from ..status_effect import StatusEffect, buff

@buff
class ImpromptuEffect(StatusEffect):
    DESCRIPTION = "Increases Max HP by 120%, stackable for 2 stacks"

    def __init__(self, name, duration, max_stacks = 2):
        super().__init__(name, duration, max_stacks)

    def apply(self, target):
        super().apply(target)
        target.max_hp
