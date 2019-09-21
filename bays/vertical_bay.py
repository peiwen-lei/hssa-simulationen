from bays.common import Bay, Container


class VerticalBay(Bay):

    def get_max_weight_level(self):
        return self.width

    def get_count_by_weight_level(self, weight_level):
        return self.height

    def put(self, container):
        col_idx = self.width - container.weight_level
        target_y_idx = self.stacks[col_idx].get_available_index()
        extra_y_move = 0
        for i in range(col_idx):
            extra_y_move = max(extra_y_move, self.stacks[i].get_available_index() - target_y_idx)
        s = self.stacks[col_idx]
        s.put(container)
        self._available_slots.update(s)
        return extra_y_move
