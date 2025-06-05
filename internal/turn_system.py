"""Turn system"""

import heapq
import uuid
from internal.entities import Entity
from internal.types import number

AV_K_VALUE = 10000
ENEMY_BASE_SPD = 50

FIRST_CYCLE_AV = 200
CYCLE_AV = 150


def base_av(spd: number):
    """Get base AV by SPD"""
    return AV_K_VALUE / spd


def modify_av_by_speed(old_av: number, spd_old: number, spd_new: number):
    """Modify Action Value by SPD"""
    return old_av * (spd_old / spd_new)


def advance(
    old_av: number, baseav: number, av_advance: number = 0, av_delay: number = 0
):
    """Advance/delay action"""
    return max(0, old_av - baseav * (av_advance - av_delay))


class Action:
    """Action class"""

    def __init__(
        self, action_id: str, value: number, source: Entity, priority: int, __value=-1
    ):
        self.id = action_id  # Unique identifier for the action
        self.value = value  # Lower value means earlier turn
        self.base_value = value if __value == -1 else __value
        self.source = source  # Pointer to the actor (can be character/summon/enemy)
        self.priority = priority

    def __lt__(self, other: "Action"):
        return (
            self.value < other.value
            if self.value != other.value
            else self.priority < other.priority
        )


class ActionQueue:
    """Action Order"""

    def __init__(self):
        self.queue: list[Action] = []  # Min-heap based on action value
        self.lookup: dict[str, Action] = {}  # Map action_id to Action
        self.total_av = 0
        self.cycles = 0
        self.current_cycle_av = FIRST_CYCLE_AV
        self.total_actions = 0

    def add_action_by_value(self, source: Entity, value: number, acting_id: str = ""):
        """Add action (frmo values) to current action order"""
        action_id = (
            str(uuid.uuid4()) if acting_id == "" else acting_id
        )  # Generate unique ID
        action = Action(action_id, value, source, priority=self.total_actions)
        heapq.heappush(self.queue, action)
        self.total_actions += 1
        self.lookup[action_id] = action
        return action_id

    def add_action(self, action: Action):
        """Add action to current action order"""
        action.value = action.base_value
        heapq.heappush(self.queue, action)
        self.total_actions += 1
        self.lookup[action.id] = action
        return action.id

    def get_next_action(self):
        """Get next action"""
        if not self.queue:
            return None
        return self.queue[0]

    def pop_next_action(self):
        """Return and pop next action"""
        if not self.queue:
            return None
        min_value = self.queue[0].value

        for action in self.queue:
            action.value -= min_value

        self.current_cycle_av -= min_value
        self.total_av += min_value

        if self.current_cycle_av <= 0:
            self.current_cycle_av = CYCLE_AV
            self.cycles += 1

        next_action = heapq.heappop(self.queue)
        del self.lookup[next_action.id]
        return next_action

    def pop_reinsert(self):
        """Return, pop, and reinsert next action"""
        action = self.pop_next_action()
        self.add_action_by_value(action.source, action.base_value, acting_id=action.id)
        return action

    def update_action_value(self, action_id, new_value):
        """Update an action's AV"""
        if action_id not in self.lookup:
            raise ValueError("Action ID not found")
        action = self.lookup[action_id]
        action.value = new_value
        heapq.heapify(self.queue)  # Re-sort the heap

    def remove_action(self, action_id):
        """Remove an action"""
        if action_id not in self.lookup:
            return
        action = self.lookup[action_id]
        self.queue.remove(action)
        heapq.heapify(self.queue)
        del self.lookup[action_id]

    def predict_next_turn_index(self, action: Action):
        """Predict when will an action takes turn after this action lasts"""

        # Snapshot current actions
        snapshot = [Action(a.id, a.value, a.source, a.priority) for a in self.queue]

        # Simulate reinsertion
        target_action = action
        predicted = Action(
            target_action.id,
            target_action.base_value,
            target_action.source,
            target_action.priority,
        )
        snapshot.append(predicted)

        # Sort as it would appear in timeline
        timeline = sorted(snapshot, key=lambda a: a)

        # Find first occurrence of this ID
        for i, a in enumerate(timeline):
            if a.id == action.id:
                return i

        return None

    def predict_action_index_after_update(self, action_id: str, new_av: number):
        """Predict action index after update takes place"""
        if action_id not in self.lookup:
            raise ValueError("Action ID not found")

        # Copy the current state
        snapshot = [Action(a.id, a.value, a.source, a.priority) for a in self.queue]

        # Simulate AV update
        updated_snapshot = []
        for a in snapshot:
            if a.id == action_id:
                # Create updated version
                updated_snapshot.append(
                    Action(a.id, new_av, a.source, a.priority, a.base_value)
                )
            else:
                updated_snapshot.append(a)

        # Sort predicted timeline
        predicted_timeline = sorted(updated_snapshot, key=lambda a: a)

        # Find index
        for i, a in enumerate(predicted_timeline):
            if a.id == action_id:
                return i

        return None

    def index(self, action_id: str):
        """Get index of an action"""
        if not action_id in self.lookup:
            return None
        return self.get_ordered_list().index(self.lookup[action_id])

    def get_ordered_list(self):
        """Return as ordered list"""
        return sorted(self.queue, key=lambda a: a)

    def __len__(self):
        return len(self.queue)

    def __iter__(self):
        return iter(self.get_ordered_list())

    def get_action(self, action_id: str):
        """Get specific action"""
        return self.lookup[action_id]
