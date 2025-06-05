# pylint: disable=import-error,no-member,invalid-name,missing-class-docstring,missing-function-docstring,missing-module-docstring,unused-import,global-statement,line-too-long
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
player = Hero("Hero", hp=14500, atk=1135, defense=200, spd=180, mp=100)
player.shield += 7500
enemy = Enemy("Dummy", hp=130_299_791_000, atk=500, defense=0, spd=140)
null = Entity("<NULL>", 0, 0, 0, 0)

# Turn state
action_order = ActionQueue()
action_order.add_action_by_value(player, base_av(player.spd))
action_order.add_action_by_value(enemy, base_av(enemy.spd))

enemy_shield_time = False

# Game loop
running = True
combat_log = ""
skill_set = [1, 1, 2, 1, 1, 2]
attack_index = 0

player.generic_regen("energy", 1)
screen.fill((50, 50, 50))
log_action(
    f"Cycle {action_order.cycles} | Actions {action_order.total_actions} | Total AVs {action_order.total_av} | [Q] to close",
    (50, 22),
)
draw_bars([player, enemy])
pygame.display.flip()

halting = False

def do_win():
    winner = player.name if player.is_alive() else enemy.name
    print(f"Game Over. {winner} wins!")
    pygame.display.flip()
    pygame.time.wait(2000)
    return True

def update_main():
    global enemy_shield_time

    if not player.is_alive() or not enemy.is_alive():
        return do_win()

    attacker_action = action_order.pop_next_action()
    attacker = attacker_action.source
    defender = "<NULL>"
    this_dmg = 0

    if isinstance(attacker, Enemy):
        pygame.time.wait(1000)
        defender = player
        this_dmg = attacker.attack(player)
        player.generic_regen("energy", raw=15)
    if isinstance(attacker, Character):
        pygame.time.wait(750 + random.randint(0, 500))
        if attacker.energy == attacker.ult_encost:
            this_dmg = attacker.ultimate(enemy)
        elif attacker.mp >= attacker.skill_mpcost:
            this_dmg = attacker.skill(target=enemy)
        else:
            this_dmg = attacker.basic_attack(enemy)
        defender = enemy

    if enemy.hp <= (enemy.max_hp * 0.25) and enemy_shield_time is False:
        enemy.shield += enemy.max_hp * 0.75
        enemy_shield_time = True

    draw_bars([player, enemy])
    log_action(
        f"{attacker.name} attacks {defender.name} for {round(this_dmg):,} damage",
        (50, 5),
    )

    if not player.is_alive() or not enemy.is_alive():
        return do_win()

    action_order.add_action_by_value(
        attacker, attacker_action.base_value, attacker_action.id
    )
    return False


while running:
    screen.fill((50, 50, 50))
    log_action(
        f"Cycle {action_order.cycles:,} | Actions {action_order.total_actions:,} | Total AVs {action_order.total_av:.1f} | [Q] to close",
        (50, 22),
    )

    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            running = False
        if event.type == pygame.KEYDOWN:
            if event.key == pygame.K_q:
                running = False
                continue

    if not halting:
        halting = update_main()
    else:
        draw_bars([player, enemy])
        log_action("Game ends", (50, 5))

    clock.tick(60)
    pygame.display.flip()

pygame.quit()
sys.exit()
