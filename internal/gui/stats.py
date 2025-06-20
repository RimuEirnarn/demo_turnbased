"""Stats-related GUI"""

from math import ceil
from typing import Iterable
from ..basic_graphics import RED, font, screen, GREEN, WHITE, BLUE
from ..entities import Entity, Character, Enemy
from .bars import Bar


def draw_basic(entity: Entity, current_index: int, focus: Entity = None):
    """Draw basic bars"""
    y = 50 + current_index * 150
    name_text = font.render(
        f"{entity.name}", True, WHITE if entity is not focus else RED
    )
    hp_text = font.render(
        f"{round(entity.hp):,}",
        True,
        WHITE,
    )
    hp_bar = Bar(50, y + 25, 200, 20, entity.max_hp, entity.hp, BLUE, border_width=0)
    shield_bar = Bar(
        50 - 4,
        y + 25 - 4,
        200 + 8,
        20 + 8,
        entity.max_hp,
        entity.shield,
        WHITE,
        border_width=0,
    )
    if entity.shield:
        shield_text = font.render(f"+{round(entity.shield):,}", True, WHITE)
        screen.blit(shield_text, (330, y + 50))
    screen.blit(name_text, (50, y))
    screen.blit(hp_text, (270, y + 25))
    shield_bar.draw(screen)
    hp_bar.draw(screen)
    return y

def draw_enemy(entity: Entity, current_index: int, focus: Entity = None):
    """Draw Enemy bars"""
    y = draw_basic(entity, current_index, focus)
    hp_percent = font.render(f"{ceil(entity.hp/entity.max_hp*100)}%", True, WHITE)
    screen.blit(hp_percent, (270, y + 55))

def draw_player(entity: Character, current_index: int, focus: Entity = None):
    """Draw Player bars"""
    y = draw_basic(entity, current_index, focus)

    mp_bar = Bar(50, y + 55, 150, 20, entity.max_mp, entity.mp, GREEN, border_width=0)
    mp_text = font.render(f"{round(entity.mp)}/{round(entity.max_mp)}", True, WHITE)
    energy_bar = Bar(
        50, y + 80, 150, 20, entity.max_energy, entity.energy, WHITE, border_width=0
    )
    energy_text = font.render(
        f"{round(entity.energy/entity.max_energy*100)}%", True, WHITE
    )
    mp_bar.draw(screen)
    energy_bar.draw(screen)
    screen.blit(mp_text, (mp_bar.x + mp_bar.width + 20, y + 55))
    screen.blit(energy_text, (energy_bar.x + energy_bar.width + 20, y + 80))


def draw_bars(iterables: Iterable[Entity], focus: Entity = None):
    """Draw bars"""
    for i, entity in enumerate(iterables):
        if isinstance(entity, Enemy):
            draw_enemy(entity, i, focus)
        if isinstance(entity, Character):
            draw_player(entity, i, focus)
