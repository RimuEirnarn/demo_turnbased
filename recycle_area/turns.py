# pylint: disable=missing-function-docstring,missing-module-docstring,wrong-import-position,invalid-name
from math import ceil
import sys
import os.path
import pygame

import tabulate


sys.path.append(os.path.abspath("./"))

from internal.types import number
from internal.turn_system import Action, ActionQueue, advance, base_av, ENEMY_BASE_SPD

pygame.quit()  # pylint: disable=no-member

# Example actors

actors = [
    {"type": "enemy", "name": "Goblin 1", "spd": ENEMY_BASE_SPD * 2},
    {"type": "character", "name": "Hero", "spd": 400},
    {"type": "summon", "name": "Fire Sprite", "spd": 230},
    {"type": "character", "name": "Healer", "spd": 200},
    {"type": "character", "name": "Support slow", "spd": 95},
    {"type": "character", "name": "Support FAST", "spd": 180},
    {"type": "character", "name": "Sub-DPS", "spd": 340},
    {"type": "enemy", "name": "Goblin 2", "spd": ENEMY_BASE_SPD * 2},
    {"type": "enemy", "name": "Goblin 3", "spd": ENEMY_BASE_SPD * 2},
    {"type": "enemy", "name": "Goblin 4", "spd": ENEMY_BASE_SPD * 2},
    {"type": "enemy", "name": "Goblin 5", "spd": ENEMY_BASE_SPD * 2},
]

# Create the queue
q = ActionQueue()

for actor in actors:
    q.add_action(actor, base_av(actor["spd"]))


def safe_input():
    r = input()
    print("\033[2K\r\033[1A", end="")
    return "0" if not r else r[0]


hero = None
enemy = None
sub_dps = None
adv = 0.7
loop = 0


def advg(acting_actor: Action, adv_value: number = 0, adv_delay: number = 0):
    new_av = advance(acting_actor.value, acting_actor.base_value, adv_value, adv_delay)
    prev_av = acting_actor.value
    adv_index = q.predict_action_index_after_update(acting_actor.id, new_av)
    print(
        f"Advancing {acting_actor.source['name']} by {(adv_value-adv_delay)*100:.0f}%, from {ceil(prev_av)} -> {ceil(new_av)}, positioning in {adv_index} ticks"
    )
    q.update_action_value(acting_actor.id, new_av)


# Process turns
while True:
    subdps = False
    next_act: Action = q.pop_reinsert()
    if next_act.source["name"] == "Hero":
        hero = next_act
    if next_act.source["name"] == "Sub-DPS":
        subdps = True
        sub_dps = next_act
    if next_act.source["name"] == "Goblin 1":
        enemy = next_act
    next_index = q.predict_next_turn_index(next_act.id)
    msg = (
        "Will act immediately"
        if next_index == 0
        else f"Will act in {next_index+1} ticks"
    )
    print(f"\n{next_act.source['name']} acts. {msg}")
    print(
        tabulate.tabulate(
            (
                (index + 1, act.source["name"], ceil(act.value), round(act.value, 4))
                for index, act in enumerate(q)
            ),
            headers=("Ticks", "Name", "AV"),
            tablefmt="simple_outline",
        )
    )
    if subdps:
        hero = q.get_action(hero.id)
        sub_dps = q.get_action(sub_dps.id)
        advg(hero, adv)
        advg(sub_dps, 0.5)
        if enemy:
            enemy = q.get_action(enemy.id)
            advg(enemy, 0, 2)

    if safe_input()[0] == "q":
        break

    loop += 1
