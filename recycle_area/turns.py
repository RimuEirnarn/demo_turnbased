import sys
import os.path

sys.path.append(os.path.abspath("./"))

from internal.turn_system import ActionQueue, base_av

# Example actors
enemy = {"type": "enemy", "name": "Goblin"}
player = {"type": "character", "name": "Hero"}
summon = {"type": "summon", "name": "Fire Sprite"}

# Create the queue
q = ActionQueue()

# Add actions
enemy_id = q.add_action(enemy, base_av(20))
player_id = q.add_action(player, base_av(200))
summon_id = q.add_action(summon, base_av(20))

def safe_input():
    r = input()
    print('\033[2K\r\033[1A', end="")
    return "0" if not r else r[0]

# Process turns
while True:
    next_act = q.pop_next_action()
    q.add_action(next_act.source, base_av(next_act.base_value))
    acts = " | ".join((f"{act.source['name']} -> {act.value}" for act in q))
    print(f"{next_act.source['name']} acts with priority {next_act.base_value} | {acts}")
    if safe_input()[0] == 'q':
        break
