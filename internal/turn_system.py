"""Turn system"""

import heapq
import uuid
from internal.types import number

AV_K_VALUE = 10000
ENEMY_BASE_SPD = 50

def base_av(spd: number):
    """Get base AV by SPD"""
    return AV_K_VALUE / spd


def modify_av_by_speed(old_av: number, spd_old: number, spd_new: number):
    """Modify Action Value by SPD"""
    return old_av * (spd_old / spd_new)


def advance(old_av: number, baseav: number, av_advance: number, av_delay: number):
    """Advance/delay action"""
    return max(0, old_av - baseav * (av_advance - av_delay))


class Action:
    """Action class"""
    def __init__(self, action_id, value, source):
        self.id = action_id  # Unique identifier for the action
        self.value = value   # Lower value means earlier turn
        self.source = source  # Pointer to the actor (can be character/summon/enemy)

    def __lt__(self, other):
        return self.value < other.value  # Needed for heapq

class ActionQueue:
    """Action Order"""
    def __init__(self):
        self.queue = []  # Min-heap based on action value
        self.lookup = {}  # Map action_id to Action

    def add_action(self, source, value):
        action_id = str(uuid.uuid4())  # Generate unique ID
        action = Action(action_id, value, source)
        heapq.heappush(self.queue, action)
        self.lookup[action_id] = action
        return action_id

    def get_next_action(self):
        if not self.queue:
            return None
        return self.queue[0]

    def pop_next_action(self):
        if not self.queue:
            return None
        action = heapq.heappop(self.queue)
        del self.lookup[action.id]
        return action

    def update_action_value(self, action_id, new_value):
        if action_id not in self.lookup:
            raise ValueError("Action ID not found")
        action = self.lookup[action_id]
        action.value = new_value
        heapq.heapify(self.queue)  # Re-sort the heap

    def remove_action(self, action_id):
        if action_id not in self.lookup:
            return
        action = self.lookup[action_id]
        self.queue.remove(action)
        heapq.heapify(self.queue)
        del self.lookup[action_id]

    def get_ordered_list(self):
        return sorted(self.queue, key=lambda a: a.value)

    def __len__(self):
        return len(self.queue)
