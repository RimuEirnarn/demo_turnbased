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
enemy = Enemy("Dummy", hp=1_250_130_299_791_000, atk=500, defense=0, spd=140)
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
time_index = 0
timed = [
    (2000, 1000, 750, (0, 500)),  # Normal
    (1000, 500, 375, (0, 250)),  # Fast
    (500, 250, 188, (0, 63)),  # Faster
    (250, 63, 94, (0, 32)),  # Even Faster
    (63, 32, 47, (0, 16)),  # Fast Deluxe
    (32, 16, 24, (0, 8)),  # Fast Premium
    (16, 8, 12, (0, 4)),  # Fast Ultimate
    (8, 4, 6, (0, 2)),  # Fast Pro
    (4, 2, 3, (0, 1)), # Fast Pro Max
    (0, 0, 0, (0, 0)) # Fastest
]
time_label = [
    "Normal",
    "Fast (2x)",
    "Faster (4x)",
    "Even Faster (8x)",
    "Fast Deluxe (16x)",
    "Fast Premium (32x)",
    "Fast Ultimate (64x)",
    "Fast Pro Max (128x)",
    "Fastest"
]

player.generic_regen("energy", 1)
screen.fill((50, 50, 50))
log_action(
    f"Cycle {action_order.cycles} | Actions {action_order.total_actions} | Total AVs {action_order.total_av:,.1f} | [Q] to close | Fast Index: {time_label[time_index]}",
    (50, 22),
)
draw_bars([player, enemy])
pygame.display.flip()

halting = False


def do_win():
    winner = player.name if player.is_alive() else enemy.name
    print(f"Game Over. {winner} wins!")
    pygame.display.flip()
    pygame.time.wait(timed[time_index][0])
    return True


def update_main():
    global enemy_shield_time

    if not player.is_alive() or not enemy.is_alive():
        return do_win()

    if action_order.cycles % 10 == 0 and action_order.cycles != 0:
        player.crit_dmg += 2
        player.max_hp += 500
        enemy.atk += 100
        # player.defense += 0.5

    if action_order.cycles % 5 == 0 and action_order.cycles != 0:
        player.crit_dmg += 1
        player.max_hp += 250

    if action_order.cycles % 50 == 0 and action_order.cycles != 0:
        player.crit_dmg += 10
        player.max_hp += 2500

    if action_order.cycles % 100 == 0 and action_order.cycles != 0:
        player.crit_dmg += 200
        player.max_hp += 5000

    if action_order.cycles % 500 == 0 and action_order.cycles != 0:
        player.crit_dmg += 100
        player.max_hp += 25000

    if action_order.cycles % 1000 == 0 and action_order.cycles != 0:
        player.crit_dmg += 2000
        player.max_hp += 50000

    attacker_action = action_order.pop_next_action()
    attacker = attacker_action.source
    defender = "<NULL>"
    this_dmg = 0

    if isinstance(attacker, Enemy):
        pygame.time.wait(timed[time_index][1])
        defender = player
        this_dmg = attacker.attack(player)
        player.generic_regen("energy", raw=5)
    if isinstance(attacker, Character):
        pygame.time.wait(timed[time_index][2] + random.randint(*timed[time_index][3]))
        if attacker.energy == attacker.ult_encost:
            this_dmg = attacker.ultimate(enemy)
        elif attacker.mp >= attacker.skill_mpcost:
            this_dmg = attacker.skill(target=enemy)
        else:
            this_dmg = attacker.basic_attack(enemy)
        defender = enemy

    if enemy.hp <= (enemy.max_hp * 0.5) and enemy_shield_time is False:
        enemy.shield += enemy.max_hp * 15
        enemy_shield_time = True

    if enemy.hp <= (enemy.max_hp * 0.25) and enemy_shield_time is True:
        enemy.shield += 20 * enemy.max_hp
        enemy_shield_time = None

    draw_bars([player, enemy], attacker)
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
        f"Cycle {action_order.cycles:,} | Actions {action_order.total_actions:,} | Total AVs {action_order.total_av:,.1f} | [Q] to close | Fast Index: {time_label[time_index]}",
        (50, 22),
    )

    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            running = False
        if event.type == pygame.KEYDOWN:
            if event.key == pygame.K_q:
                running = False
                continue
            if event.key == pygame.K_0:
                time_index = 0
            if event.key == pygame.K_1:
                time_index = 1
            if event.key == pygame.K_2:
                time_index = 2
            if event.key == pygame.K_3:
                time_index = 3
            if event.key == pygame.K_4:
                time_index = 4
            if event.key == pygame.K_5:
                time_index = 5
            if event.key == pygame.K_6:
                time_index = 6
            if event.key == pygame.K_7:
                time_index = 7
            if event.key == pygame.K_8:
                time_index = 8

    if not halting:
        halting = update_main()
    else:
        draw_bars([player, enemy])
        log_action("Game ends", (50, 5))

    clock.tick(60)
    pygame.display.flip()

pygame.quit()
sys.exit()
