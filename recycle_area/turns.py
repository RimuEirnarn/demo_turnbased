# pylint: disable=missing-function-docstring,missing-module-docstring,wrong-import-position,invalid-name,line-too-long
from math import ceil
import sys
import os.path
from typing import TypeVar, Type
import pygame

import tabulate


sys.path.append(os.path.abspath("./"))

from internal.types import number
from internal.turn_system import Action, ActionQueue, advance, base_av, ENEMY_BASE_SPD

pygame.quit()  # pylint: disable=no-member

T = TypeVar("T")

# Example actors

actors = [
    {"type": "enemy", "name": "Goblin 1", "spd": ENEMY_BASE_SPD * 2},
    {"type": "character", "name": "Hero", "spd": 125},
    {"type": "summon", "name": "Fire Sprite", "spd": 130},
    {"type": "character", "name": "Healer", "spd": 133},
    {"type": "character", "name": "Support slow", "spd": 92},
    {"type": "character", "name": "Support FAST", "spd": 162},
    {"type": "character", "name": "Sub-DPS", "spd": 180},
    {"type": "enemy", "name": "Goblin 2", "spd": ENEMY_BASE_SPD * 2},
    {"type": "enemy", "name": "Goblin 3", "spd": ENEMY_BASE_SPD * 2},
    {"type": "enemy", "name": "Goblin 4", "spd": ENEMY_BASE_SPD * 2},
    {"type": "enemy", "name": "Goblin 5", "spd": ENEMY_BASE_SPD * 2},
]

# Create the queue
q = ActionQueue()

for _actor in actors:
    q.add_action_by_value(_actor, base_av(_actor["spd"]))


def safe_input():
    r = input()
    print("\033[2K\r\033[1A", end="")
    return "0" if not r else r[0]

def input_cast(prompt: str, type_: Type[T], default: T = None) -> T:
    r = input(prompt)
    try:
        return type_(r)
    except (ValueError, TypeError):
        return default

hero = None
enemy = None
sub_dps = None
slow = None
adv = 0.7
loop = 0


def advance_actor():
    name = input("Name? ")
    if not name:
        return
    advance_value = input_cast("Value (%)? ", int)
    actor_names = tuple((act.source['name'] for act in q.get_ordered_list()))
    if not name in actor_names:
        print("No name in entry")
        return
    actor = q.get_ordered_list()[actor_names.index(name)]
    advg(actor, advance_value/100)

def system_quit():
    return True

MENU_ACTION = {
    1: ("Advance actor", advance_actor),
    "q": ("Quit", system_quit)
}

def advg(acting_actor: Action, adv_value: number = 0, adv_delay: number = 0):
    new_av = advance(acting_actor.value, acting_actor.base_value, adv_value, adv_delay)
    prev_av = acting_actor.value
    adv_index = q.predict_action_index_after_update(acting_actor.id, new_av)
    prev_index: int = q.index(acting_actor.id)

    message = (
        f"Positioning in {adv_index+1} ticks from {prev_index+1} tick"
        if adv_index != 0
        else f"Will act on next action from {prev_index+1} tick"
    )
    action_advance = (adv_value - adv_delay) * 100
    name = acting_actor.source["name"]
    print(
        f"Advancing {name} by {action_advance:.0f}%, from {ceil(prev_av)} -> {ceil(new_av)}. {message}"
    )
    q.update_action_value(acting_actor.id, new_av)


def show(action_order: ActionQueue | tuple):
    print(
        tabulate.tabulate(
            (
                (index + 1, act.source["name"], ceil(act.value), round(act.base_value, 6))
                for index, act in enumerate(action_order)
            ),
            headers=("Ticks", "Name", "AV", "Base AV"),
            tablefmt="simple_outline",
        )
    )

def show_menu():
    sels = "\n".join(f"[{input_selection}]: {data[0]}" for input_selection, data in MENU_ACTION.items())
    select = input(f"""\
Select action:
{sels}
> """)

    if not select in MENU_ACTION:
        return
    return MENU_ACTION[select][1]()

# Process turns
while True:
    subdps = False
    next_act: Action = q.pop_next_action()
    if next_act.source["name"] == "Hero":
        hero = next_act
    if next_act.source["name"] == "Sub-DPS":
        subdps = True
        sub_dps = next_act
    if next_act.source["name"] == "Goblin 1":
        enemy = next_act
    if next_act.source['name'] == "Support slow":
        slow = next_act
    next_index = q.predict_next_turn_index(next_act)
    msg = (
        "Will act immediately"
        if next_index == 0
        else f"Will act in {next_index+1} ticks"
    )
    # pre = tuple(q)
    print(
        f"\n[Action {loop+1} | Cycle {q.cycles} ({q.current_cycle_av:.0f})] {next_act.source['name']} acts. {msg}"
    )
    q.add_action(next_act)
    if subdps and hero:

        hero = q.get_action(hero.id)
        sub_dps = q.get_action(sub_dps.id)
        advg(hero, adv)
        advg(sub_dps, 0.5)

        if slow:
            slow = q.get_action(slow.id)
            advg(slow, adv)

    show(q)
    if show_menu():
        break
    # t = safe_input()
    # if t[0] == "q":
    #     break
    # if t[0] == "a":
        # print(f"Total AVs for this battle is: {q.total_av}")

    loop += 1
