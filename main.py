# pylint: disable=import-error,no-member,invalid-name,missing-class-docstring,missing-function-docstring,missing-module-docstring,unused-import
import sys
from math import ceil
import random
import pygame

from internal.basic_graphics import screen, BLACK, log_action, clock
from internal.characters.hero import Hero
from internal.entities import Enemy, Character, Entity
from internal.gui.stats import draw_bars
from internal.turn_system import ActionQueue, base_av

# Demo characters
player = Hero("Hero", hp=3210, atk=2135, defense=490, spd=200, mp=100)
player.shield += 7500
enemy = Enemy("Dummy", hp=13_299_791_000, atk=500, defense=0, spd=20)
null = Entity("<NULL>", 0, 0, 0, 0)

# Turn state
action_order = ActionQueue()
action_order.add_action(player, base_av(player.spd))
action_order.add_action(enemy, base_av(enemy.spd))
turn_order = sorted([player, enemy], key=lambda x: x.spd, reverse=True)
turn_index = 0

# Game loop
running = True
combat_log = ""
skill_set = [1, 1, 2, 1, 1, 2]
attack_index = 0

while running:
    screen.fill((50, 50, 50))
    draw_bars([player, enemy])
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            running = False
        if event.type == pygame.KEYDOWN:
            if event.key == pygame.K_q:
                running = False
                continue

    attacker_action = action_order.pop_next_action()
    attacker = attacker_action.source
    defender = "<NULL>"
    skill_name = null
    this_dmg = 0

    if not player.is_alive() or not enemy.is_alive():
        winner = player.name if player.is_alive() else enemy.name
        print(f"Game Over. {winner} wins!")
        pygame.time.wait(2000)
        running = False
        continue

    if isinstance(attacker, Enemy):
        pygame.time.wait(1000)
        defender = player
        this_dmg = attacker.attack(player)
        skill_name = "Enemy: Basic Attack"
    if isinstance(attacker, Character):
        pygame.time.wait(750 + random.randint(0, 500))
        if attacker.energy == attacker.ult_encost:
            this_dmg = attacker.ultimate(enemy)
        elif attacker.mp >= attacker.skill_mpcost:
            this_dmg = attacker.skill(target=enemy)
        else:
            this_dmg = attacker.basic_attack(enemy)
        defender = enemy
    log_action(
        f"{attacker.name} attacks {defender.name} for {round(this_dmg):,} damage",
        (50, 5),
    )

    turn_index += 1
    action_order.add_action(attacker, attacker_action.base_value, attacker_action.id)
    clock.tick(60)
    pygame.display.flip()

pygame.quit()
sys.exit()
