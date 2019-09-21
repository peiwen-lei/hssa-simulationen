import unittest
from bays.common import Stack, Container


class StackTest(unittest.TestCase):

    def test_stack_is_full_after_multiple_put(self):
        s = Stack(2, 0)
        s.put(Container(1, 1))
        s.put(Container(1, 1))
        self.assertTrue(s.is_full())

    def test_stack_find(self):
        s = Stack(3, 0)
        s.put(Container(1, 1))
        s.put(Container(2, 1))
        s.put(Container(3, 1))
        self.assertEqual(s.find_by_weight(3), 2)
        self.assertEqual(s.find_by_weight(2), 1)
        self.assertEqual(s.find_by_weight(1), 0)

    def test_stack_get(self):
        s = Stack(3, 0)
        s.put(Container(1, 1))
        s.put(Container(2, 1))
        s.put(Container(3, 1))
        self.assertEqual(s.get(0), Container(1, 1))
        self.assertEqual(s.get(1), Container(2, 1))
        self.assertEqual(s.get(2), Container(3, 1))

    def test_stack_get_available(self):
        s = Stack(3, 0)
        self.assertEqual(s.get_available_index(), 0)
        s.put(Container(1, 1))
        s.put(Container(2, 1))
        s.put(Container(3, 1))
        self.assertEqual(s.get_available_index(), 3)


if __name__ == '__main__':
    unittest.main()
