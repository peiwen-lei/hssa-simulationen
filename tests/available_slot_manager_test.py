import unittest
from bays.common import Stack, Container, AvailableSlotManger, Slot


class AvailableSlotManagerTest(unittest.TestCase):

    def test_manager_initialization(self):
        stacks = [Stack(2, 0), Stack(2, 1)]
        stacks[0].put(Container(1, 1))
        m = AvailableSlotManger(stacks)
        available_slots = m.get()
        self.assertEqual(available_slots, {0: Slot(0, 1), 1: Slot(1, 0)})

    def test_manager_update(self):
        stacks = [Stack(3, 0), Stack(3, 1), Stack(3, 2)]
        m = AvailableSlotManger(stacks)
        stacks[0].put(Container(1, 1))
        stacks[0].put(Container(1, 1))
        stacks[1].put(Container(1, 1))
        m.update(stacks[0])
        m.update(stacks[1])
        available_slots = m.get()
        self.assertEqual(available_slots, {0: Slot(0, 2),
                                           1: Slot(1, 1),
                                           2: Slot(2, 0)})


if __name__ == '__main__':
    unittest.main()
