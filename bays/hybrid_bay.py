import math
import random
from bays.common import Bay, Slot, Point


class HybridBay(Bay):

    # Get the maximum weight level of this block
    def get_max_weight_level(self):
        return self.width + self.height - 1

    def get_count_by_weight_level(self, weight_level):
        height = self.height
        width = self.width
        return min(weight_level, height) if weight_level <= width \
            else height - (weight_level - width)

    # Return a list of tuples, which are the column and row index of the ideal slots for the container with given weight
    # The slots are always listed from left to right
    # Slot index starting from 0
    def calc_ideal_slots(self, weight_level):
        width = self.width
        count = self.get_count_by_weight_level(weight_level)
        left = max(0, width - weight_level)
        bottom = max(0, weight_level - width)
        return [Slot(left + i, bottom + i) for i in range(count)]

    # Get the geometry center of the containers with given weight level
    def get_center(self, weight_level):
        ideal_slots = self.calc_ideal_slots(weight_level)
        center = Point(0, 0)
        for slot in ideal_slots:
            center = center + slot.get_center()
        return center / len(ideal_slots)

    def put(self, container):
        available_slots = self._available_slots.get()

        if len(available_slots.keys()) == 0:
            raise Exception("Cannot put more containers, because the bay is already full!")

        # Try to find an available slot which happens to be the ideal spot
        target_slot = self.get_ideal_slot(container.weight_level, available_slots)

        if target_slot is None:
            center = self.get_center(container.weight_level)
            # Find the closest slot        
            candidates = []
            for _, slot in available_slots.items():
                # Slot is using the index, while center is in coordinates
                dist = self.calc_distance(center, slot.get_center())
                candidates.append((dist, slot))
            # TODO: here can have different prioritization: low or high
            _, target_slot = min(candidates, key=lambda t: (t[0], t[1].y_idx))
        # Calculate the extra Y direction movement needed
        extra_y_movement = 0
        for i in range(target_slot.x_idx):
            extra_y_movement = max(extra_y_movement, self.stacks[i].get_available_index() - target_slot.y_idx)
        # Update stack
        s = self.stacks[target_slot.x_idx]
        s.put(container)
        self._available_slots.update(s)
        return extra_y_movement

    # Check whether at least one ideal slot is available and return it. If none exists, return None
    # It randomly chooses one slot, if multiple ideal slots are available
    def get_ideal_slot(self, weight_level, available_slots):
        ideal_slots = self.calc_ideal_slots(weight_level)
        possible_slots = []
        for slot in ideal_slots:
            if slot.x_idx in available_slots and slot.y_idx == available_slots[slot.x_idx].y_idx:
                possible_slots.append(slot)
        if len(possible_slots) == 0:
            return None
        return random.choice(possible_slots)

    # Calculate the distance between the geometry c
    # It is on purpose that it returns an integer so that we can avoid comparing distance in float numbers
    def calc_distance(self, p1, p2):
        return int(math.pow((p1.x - p2.x) * 2, 2) + math.pow((p1.y - p2.y) * 2, 2))


# If multiple ideal location exists always pick the right one
class HybridRightBay(HybridBay):

    # Check whether at least one ideal slot is available and return it. If none exists, return None
    # It always return the left-most ideal slot, if multiple slots are available
    def get_ideal_slot(self, weight_level, available_slots):
        ideal_slots = self.calc_ideal_slots(weight_level)
        for slot in reversed(ideal_slots):
            if slot.x_idx in available_slots and slot.y_idx == available_slots[slot.x_idx].y_idx:
                return slot
        return None


# If multiple ideal location exists always pick the left one
class HybridLeftBay(HybridBay):

    # Check whether at least one ideal slot is available and return it. If none exists, return None
    # It always return the left-most ideal slot, if multiple slots are available
    def get_ideal_slot(self, weight_level, available_slots):
        ideal_slots = self.calc_ideal_slots(weight_level)
        for slot in ideal_slots:
            if slot.x_idx in available_slots and slot.y_idx == available_slots[slot.x_idx].y_idx:
                return slot
        return None
