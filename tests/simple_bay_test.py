import unittest
from bays.common import Bay, Container
from bays.random_bay import RandomBay
from bays.vertical_bay import VerticalBay


class BasicBay(Bay):

    def get_max_weight_level(self):
        pass

    def get_count_by_weight_level(self, weight_level):
        pass

    def put(self, container):
        pass


class BayTest(unittest.TestCase):

    def test_populate(self):
        b = BasicBay(4, 2)
        b.populate([
            [Container(1, 1), Container(1, 1), Container(2, 2), Container(2, 2)],
            [None, Container(2, 2), None, Container(3, 3)]
        ])
        expect_res = '(  ,  )(02,02)(  ,  )(03,03)\n' \
                     '(01,01)(01,01)(02,02)(02,02)\n'
        self.assertEqual(str(b), expect_res)

    def test_take(self):
        b = BasicBay(4, 3)
        b.populate([
            [Container(1, 1), Container(2, 2), Container(3, 3), Container(4, 4)],
            [Container(5, 5), Container(6, 6), Container(7, 7), Container(8, 8)],
            [None, Container(9, 9), None, Container(9, 9)]
        ])
        rh = b.take(3)
        self.assertEqual(rh, 1)
        expect_res = '(  ,  )(09,09)(  ,  )(09,09)\n' \
                     '(05,05)(06,06)(  ,  )(08,08)\n'  \
                     '(01,01)(02,02)(07,07)(04,04)\n'
        self.assertEqual(str(b), expect_res)
        rh = b.take(2)
        self.assertEqual(rh, 2)
        expect_res = '(  ,  )(  ,  )(  ,  )(09,09)\n' \
                     '(05,05)(09,09)(  ,  )(08,08)\n'  \
                     '(01,01)(06,06)(07,07)(04,04)\n'
        self.assertEqual(str(b), expect_res)


class RandomBayTest(unittest.TestCase):

    def test_put(self):
        b = RandomBay(4, 3)
        b.populate([
            [Container(1, 1), Container(2, 2), Container(3, 3), Container(4, 4)],
            [Container(5, 5), Container(6, 6), Container(7, 7), Container(8, 8)],
            [None, Container(9, 9), None, None]
        ])
        b.put(Container(1, 1))
        expect_res = '(  ,  )(09,09)(  ,  )(01,01)\n' \
                     '(05,05)(06,06)(07,07)(08,08)\n' \
                     '(01,01)(02,02)(03,03)(04,04)\n'
        self.assertEqual(str(b), expect_res)
        b.put(Container(2, 2))
        expect_res = '(  ,  )(09,09)(02,02)(01,01)\n' \
                     '(05,05)(06,06)(07,07)(08,08)\n' \
                     '(01,01)(02,02)(03,03)(04,04)\n'
        self.assertEqual(str(b), expect_res)


class VerticalBayTest(unittest.TestCase):

    def test_put(self):
        b = VerticalBay(4, 3)
        b.populate([
            [Container(9, 4), Container(6, 3), Container(3, 2), Container(0, 1)],
            [Container(10, 4), None, None, None]
        ])
        extra_move = b.put(Container(1, 1))
        self.assertEqual(extra_move, 1)
        expect_res = '(  ,  )(  ,  )(  ,  )(  ,  )\n' \
                     '(10,04)(  ,  )(  ,  )(01,01)\n' \
                     '(09,04)(06,03)(03,02)(00,01)\n'
        self.assertEqual(str(b), expect_res)
        extra_move = b.put(Container(4, 2))
        self.assertEqual(extra_move, 1)
        expect_res = '(  ,  )(  ,  )(  ,  )(  ,  )\n' \
                     '(10,04)(  ,  )(04,02)(01,01)\n' \
                     '(09,04)(06,03)(03,02)(00,01)\n'
        self.assertEqual(str(b), expect_res)
        extra_move = b.put(Container(11, 4))
        self.assertEqual(extra_move, 0)
        expect_res = '(11,04)(  ,  )(  ,  )(  ,  )\n' \
                     '(10,04)(  ,  )(04,02)(01,01)\n' \
                     '(09,04)(06,03)(03,02)(00,01)\n'
        self.assertEqual(str(b), expect_res)


if __name__ == '__main__':
    unittest.main()
