from math import ceil
import sys
import os.path
import pygame

import tabulate

sys.path.append(os.path.abspath("./"))

from internal.turn_system import ActionQueue, base_av, ENEMY_BASE_SPD

pygame.quit() # pylint: disable=no-member

# Example actors

actors = [
    {"type": "enemy", "name": "Goblin 1", "spd": ENEMY_BASE_SPD},
    {"type": "character", "name": "Hero", "spd": 800},
    {"type": "summon", "name": "Fire Sprite", "spd": 230},
    {"type": "character", "name": "Healer", "spd": 200},
    {"type": "character", "name": "Support slow", "spd": 95},
    {"type": "character", "name": "Support FAST", "spd": 180},
    {"type": "character", "name": "Sub-DPS", "spd": 340},
    {"type": "enemy", "name": "Goblin 2", "spd": ENEMY_BASE_SPD},
    {"type": "enemy", "name": "Goblin 3", "spd": ENEMY_BASE_SPD},
    {"type": "enemy", "name": "Goblin 4", "spd": ENEMY_BASE_SPD},
    {"type": "enemy", "name": "Goblin 5", "spd": ENEMY_BASE_SPD},
]

# Create the queue
q = ActionQueue()

for actor in actors:
    q.add_action(actor, base_av(actor["spd"]))


def safe_input():
    r = input()
    print("\033[2K\r\033[1A", end="")
    return "0" if not r else r[0]


# Process turns
while True:
    next_act = q.pop_reinsert()
    next_index = q.predict_next_turn_index(next_act.id)
    msg = "Will act immediately" if next_index == 0 else f"Will act in {next_index+1} ticks"
    print(
        f"\n{next_act.source['name']} acts. {msg}"
    )
    print(
        tabulate.tabulate(
            (
                (index + 1, act.source["name"], ceil(act.value), round(act.value, 4))
                for index, act in enumerate(q)
            ),
            headers=("Ticks", "Name", "AV", "Real AV"),
            tablefmt="simple_outline",
        )
    )
    if safe_input()[0] == "q":
        break
