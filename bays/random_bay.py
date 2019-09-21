from bays.common import Bay, Container


class RandomBay(Bay):

    # Get the maximum weight level of this block
    def get_max_weight_level(self):
        return self.width

    def get_count_by_weight_level(self, weight_level):
        return self.height

    def put(self, container):
        for s in reversed(self.stacks):
            if not s.is_full():
                s.put(container)
                self._available_slots.update(s)
                return 0
        raise Exception("Cannot put more containers, because the bay is already full!")
