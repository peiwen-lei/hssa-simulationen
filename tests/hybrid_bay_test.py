import unittest
from bays.common import Slot, Point, Container
from bays.hybrid_bay import HybridBay


class HybridBayTest(unittest.TestCase):

    def test_calc_ideal_slots(self):
        b = HybridBay(4, 3)
        slots = b.calc_ideal_slots(2)
        self.assertEqual([Slot(2, 0), Slot(3, 1)], slots)
        slots = b.calc_ideal_slots(3)
        self.assertEqual([Slot(1, 0), Slot(2, 1), Slot(3, 2)], slots)

    def test_get_center(self):
        b = HybridBay(4, 3)
        c = b.get_center(2)
        self.assertEqual(Point(3.0, 1.0), c)

    def test_put_in_ideal_slots(self):
        b = HybridBay(4, 3)
        b.populate([
            [Container(6, 4), Container(3, 3), Container(1, 2), Container(0, 1)],
            [Container(9, 5), Container(7, 4), Container(4, 3), Container(2, 2)]
        ])

        extra_movement = b.put(Container(10, 5))
        self.assertEqual(0, extra_movement)
        expect_res = '(  ,  )(10,05)(  ,  )(  ,  )\n' \
                     '(09,05)(07,04)(04,03)(02,02)\n' \
                     '(06,04)(03,03)(01,02)(00,01)\n'
        self.assertEqual(expect_res, str(b))

        extra_movement = b.put(Container(5, 3))
        self.assertEqual(1, extra_movement)
        expect_res = '(  ,  )(10,05)(  ,  )(05,03)\n' \
                     '(09,05)(07,04)(04,03)(02,02)\n' \
                     '(06,04)(03,03)(01,02)(00,01)\n'
        self.assertEqual(expect_res, str(b))

    def test_put_in_closest_slots(self):
        b = HybridBay(4, 3)
        b.populate([
            [Container(6, 4), Container(3, 3), Container(1, 2), Container(0, 1)],
            [Container(9, 5), None, Container(4, 3), Container(2, 2)]
        ])

        extra_movement = b.put(Container(10, 5))
        self.assertEqual(1, extra_movement)
        expect_res = '(  ,  )(  ,  )(  ,  )(  ,  )\n' \
                     '(09,05)(10,05)(04,03)(02,02)\n' \
                     '(06,04)(03,03)(01,02)(00,01)\n'
        self.assertEqual(expect_res, str(b))

        extra_movement = b.put(Container(11, 6))
        self.assertEqual(0, extra_movement)
        expect_res = '(11,06)(  ,  )(  ,  )(  ,  )\n' \
                     '(09,05)(10,05)(04,03)(02,02)\n' \
                     '(06,04)(03,03)(01,02)(00,01)\n'
        self.assertEqual(expect_res, str(b))


if __name__ == '__main__':
    unittest.main()
