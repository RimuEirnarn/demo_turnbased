# pylint: disable=import-error,no-member,invalid-name,missing-class-docstring,missing-function-docstring,missing-module-docstring,unused-import
import sys
from math import ceil
import random
import pygame

from internal.basic_graphics import screen, BLACK, log_action, clock
from internal.characters.hero import Hero
from internal.entities import Enemy, Player
from internal.gui.stats import draw_bars

# Demo characters
player = Hero("Hero", hp=3210, atk=2135, defense=490, spd=10, mp=100)
enemy = Enemy("Dummy", hp=13_299_791_000, atk=500, defense=0, spd=5)

# Turn state
turn_order = sorted([player, enemy], key=lambda x: x.spd, reverse=True)
turn_index = 0

# Game loop
running = True
combat_log = ""
skill_set = [1, 1, 2, 1, 1, 2]
attack_index = 0

while running:
    screen.fill(BLACK)
    draw_bars([player, enemy])
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            running = False

    attacker = turn_order[turn_index % 2]
    defender = turn_order[(turn_index + 1) % 2]
    skill_name = "Null"
    this_dmg = 0

    if not attacker.is_alive() or not defender.is_alive():
        winner = attacker.name if attacker.is_alive() else defender.name
        print(f"Game Over. {winner} wins!")
        pygame.time.wait(2000)
        running = False
        continue

    if isinstance(attacker, Enemy):
        pygame.time.wait(1000)
        this_dmg = attacker.attack(defender)
        skill_name = "Enemy: Basic Attack"
    if isinstance(attacker, Player):
        pygame.time.wait(750 + random.randint(0, 500))
        if attacker.energy == attacker.ult_encost:
            this_dmg = attacker.ultimate(defender)
        elif attacker.mp >= attacker.skill_mpcost:
            this_dmg = attacker.skill(target=defender)
        else:
            this_dmg = attacker.basic_attack(defender)
    log_action(
        f"{attacker.name} attacks {defender.name} for {round(this_dmg):,} damage",
        (50, 5),
    )

    turn_index += 1
    clock.tick(60)
    pygame.display.flip()

pygame.quit()
sys.exit()
