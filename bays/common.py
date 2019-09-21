import random
from abc import ABC, abstractmethod


# A basic class for bays
class Bay(ABC):

    def __init__(self, width, height):
        self.width = width
        self.height = height
        self.stacks = [Stack(height, i) for i in range(width)]
        self._available_slots = AvailableSlotManger(self.stacks)

    @abstractmethod
    def get_max_weight_level(self):
        """
        Get the maximum container weight level for this bay
        :return: the maximum container weight level. Weight level starting from 1
        """

    @abstractmethod
    def get_count_by_weight_level(self, weight_level):
        """
        Get the number of containers in the given weight level
        :param weight_level: the weight level
        :return: the number of containers in that weight level
        """

    @abstractmethod
    def put(self, container):
        """
        Put a container into the bay
        :param container: the container to be put into the bay
        :return: the number of extra movements involved when putting the container
        """

    # Take a container with given weight out of the bay, returning the rehandling needed for this container
    def take(self, weight):
        for s in self.stacks:
            row_idx = s.find_by_weight(weight)
            if row_idx is not None:
                # rh is short for rehandling. This is the rehandling needed to retrieve the container
                rh_count = s.get_available_index() - row_idx - 1
                s.remove(row_idx)
                self._available_slots.update(s)
                return rh_count
        raise Exception(
            'Removing non-existing container with weight ' + str(weight))

    # # TODO: update this method
    # def take_by_weight_level(self, container):
    #     for s in self.stacks:
    #         row_idx = s.find_by_weight(container)
    #         if row_idx is not None:
    #             # rh is short for rehandling. This is the rehandling needed to retrieve the container
    #             rh_count = s.get_available_index() - row_idx - 1
    #             s.remove(row_idx)
    #             self._available_slots.update(s)
    #             return rh_count
    #     raise Exception(
    #         'Removing non-existing container with weight ' + str(container.weight))

    def populate(self, layers):
        for layer in layers:
            for i, container in enumerate(layer):
                if container is not None:
                    self.stacks[i].put(container)
        for s in self.stacks:
            self._available_slots.update(s)

    def __str__(self):
        res = ""
        for row in reversed(range(self.height)):
            for col in range(self.width):
                container = self.stacks[col].get(row)
                res += "(  ,  )" if container is None else str(container)
            res += "\n"
        return res

    def __eq__(self, other):
        if not isinstance(other, Bay):
            return False

        if self.width != other.width or self.height != other.height:
            return False
        for c in range(self.width):
            for r in range(self.height):
                if self.stacks[c].get(r) != other.stacks[c].get(r):
                    print(self.stacks[c].get(r))
                    print(other.stacks[c].get(r))
                    return False
        return True


# A class representing one stack in a block
class Stack:

    def __init__(self, height, index):
        self.index = index
        self._height = height
        self._slots = []

    # Put a container into the stack
    # Return the new available index for this stack
    def put(self, container):
        if self.is_full():
            raise Exception('Stack ' + str(self.index) + ' is already full!')
        else:
            self._slots.append(container)
            return self.get_available_index()

    # Get the currently available slot index in this stack
    def get_available_index(self):
        return len(self._slots)

    # Check whether this stack is full
    def is_full(self):
        return len(self._slots) >= self._height

    # Find a container with given weight in this stack and returns its index
    def find_by_weight(self, weight):
        for c in reversed(self._slots):
            if c.weight == weight:
                return self._slots.index(c)
        return None

    # Get the container in the given index
    def get(self, index):
        if len(self._slots) > index:
            return self._slots[index]
        else:
            return None

    def remove(self, idx):
        return self._slots.pop(idx)


# A class which manages a list of currently available
class AvailableSlotManger:

    def __init__(self, stacks):
        # _slots is an internal dictionary with the stack index being the key,
        # and the available slot index on that stack as the value.
        # If the stack is full, its value is set to -1
        self._slots = {}
        for s in stacks:
            self._slots[s.index] = -1 if s.is_full() \
                else s.get_available_index()

    def update(self, stack):
        self._slots[stack.index] = -1 if stack.is_full() \
            else stack.get_available_index()

    def get(self):
        return {x_idx: Slot(x_idx, y_idx) for x_idx, y_idx in self._slots.items() if y_idx >= 0}


# A class representing the a single slot in a place. It has x index and y index
class Slot:

    def __init__(self, x_idx, y_idx):
        self.x_idx = x_idx
        self.y_idx = y_idx

    def get_center(self):
        return Point(self.x_idx + 0.5, self.y_idx + 0.5)

    def __eq__(self, other):
        return self.x_idx == other.x_idx and self.y_idx == other.y_idx


# A class representing a point in the coordinate system
class Point:

    def __init__(self, x, y):
        self.x = x
        self.y = y

    def __add__(self, other):
        x = self.x + other.x
        y = self.y + other.y
        return Point(x, y)

    def __mul__(self, scalar):
        return Point(self.x * scalar, self.y * scalar)

    def __truediv__(self, scalar):
        return Point(self.x / scalar, self.y / scalar)

    def __eq__(self, other):
        return self.x == other.x and self.y == other.y


# A class representing the container
# A container has two attributes:
#   1. weight: starting from 0
#   2. weight level: starting from 1
class Container:

    def __init__(self, weight, weight_level):
        self.weight = weight
        self.weight_level = weight_level

    def __eq__(self, other):
        return self.weight == other.weight and self.weight_level == other.weight_level

    def __str__(self):
        return '({0:02d},{1:02d})'.format(self.weight, self.weight_level)


# A class representing a sequence of container
class ContainerGenerator:

    def __init__(self, total, is_random):
        self._sequence = list(reversed(range(total)))
        if is_random:
            random.shuffle(self._sequence)

    def get_iterator(self, bay):
        return ContainerGeneratorIterator(bay, self._sequence)


# A class which generate containers in different weight level according to the given sequence
class ContainerGeneratorIterator:

    def __init__(self, bay, sequence):
        self._bay = bay
        weight_level_list = self.create_weight_level_list()
        self._containers = [Container(i, weight_level_list[i]) for i in sequence]
        # This variable is only meant to be used for iterating
        self._iter_tracker = 0

    def create_weight_level_list(self):
        bay = self._bay
        total = bay.height * bay.width
        # Make a list
        weight_level_list = []
        index = 0
        weight = 1
        while index < total:
            count = bay.get_count_by_weight_level(weight)
            for _ in range(0, count):
                weight_level_list.append(weight)
                index += 1
            weight += 1
        return weight_level_list[:total]

    def __iter__(self):
        return iter(self._containers)

    def __next__(self):
        next(self._containers)
