import unittest
from bays.common import ContainerGenerator, ContainerGeneratorIterator, Container
from bays.hybrid_bay import HybridBay
from bays.random_bay import RandomBay
from bays.vertical_bay import VerticalBay


class StackTest(unittest.TestCase):

    def test_generator_generate_reversed_list_when_not_random(self):
        g = ContainerGenerator(5, False)
        self.assertEqual(g._sequence, [4, 3, 2, 1, 0])

    def test_generator_generate_reversed_list_when_random(self):
        g1 = ContainerGenerator(10, True)
        g2 = ContainerGenerator(10, True)
        self.assertNotEqual(g1._sequence, g2._sequence)

    def test_iterator_weight_level_list_generation(self):
        g = ContainerGenerator(12, False)

        b1 = HybridBay(4, 3)
        l1 = g.get_iterator(b1).create_weight_level_list()
        self.assertEqual(l1, [1, 2, 2, 3, 3, 3, 4, 4, 4, 5, 5, 6])

        b2 = RandomBay(4, 3)
        l2 = g.get_iterator(b2).create_weight_level_list()
        self.assertEqual(l2, [1, 1, 1, 2, 2, 2, 3, 3, 3, 4, 4, 4])

        b3 = VerticalBay(4, 3)
        l3 = g.get_iterator(b3).create_weight_level_list()
        self.assertEqual(l3, [1, 1, 1, 2, 2, 2, 3, 3, 3, 4, 4, 4])

    def test_iterator_container_generation(self):
        b = HybridBay(3, 2)
        it = ContainerGenerator(6, False).get_iterator(b)
        self.assertEqual(
            list(it),
            [Container(5, 4), Container(4, 3), Container(3, 3),
             Container(2, 2), Container(1, 2), Container(0, 1)]
        )


if __name__ == '__main__':
    unittest.main()
