"""Stats-related GUI"""
from math import ceil
from ..basic_graphics import font, screen, GREEN, RED, WHITE
from ..entities import Entity, Character, Enemy

def draw_basic(entity: Entity, current_index: int):
    y = 50 + current_index * 100
    name_text = font.render(f"{entity.name}", True, WHITE)
    hp_text = font.render(
        f"HP: {round(entity.hp):,}/{round(entity.max_hp):,} ({ceil(entity.hp/entity.max_hp*100)}%)",
        True,
        RED,
    )
    screen.blit(name_text, (50, y))
    screen.blit(hp_text, dest=(50, y + 25))
    return y


def draw_player(entity: Character, current_index: int):
    y = draw_basic(entity, current_index)
    mp_text = font.render(f"MP: {round(entity.mp)}/{round(entity.max_mp)}", True, GREEN)
    energy_text = font.render(
        f"Energy: {round(entity.energy)}/{round(entity.max_energy)} ({round(entity.energy/entity.max_energy*100)}%)",
        True,
        GREEN,
    )
    screen.blit(mp_text, dest=(50, y + 50))
    screen.blit(energy_text, dest=(50, y + 65))


def draw_bars(iterables):
    for i, entity in enumerate(iterables):
        if isinstance(entity, Enemy):
            draw_basic(entity, i)
        if isinstance(entity, Character):
            draw_player(entity, i)
