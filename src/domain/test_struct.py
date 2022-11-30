import unittest
from src.domain.struct import Iterable, sort_data, filter_data
from copy import deepcopy


class Test(unittest.TestCase):

    def test_class(self):
        data = Iterable()

        sort_data(data, lambda x, y: x < y)
        self.assertEqual(data, [])

        data.append(1)
        self.assertEqual(data, [1])

        result = filter_data(data, lambda x: x == 10)
        self.assertEqual(result, [])

        sort_data(data, lambda x, y: x < y)
        self.assertEqual(data, [1])

        data[1] = 1
        self.assertEqual(data, [1, 1])

        data[0] = 0
        self.assertEqual(data, [0, 1])

        self.assertEqual(data[0], 0)

        del data[1]
        self.assertEqual(data, [0])

        data[1] = 1
        data.remove(1)
        self.assertEqual(data, [0])

        try:
            data[2] = 2
        except IndexError:
            pass

        self.assertEqual(len(data), 1)

        data.append(1)
        data.append(2)
        data.append(3)
        data.append(4)
        data.append(5)

        info = deepcopy(data)

        sort_data(info, lambda x, y: x < y)
        self.assertEqual(info, [0, 1, 2, 3, 4, 5])

        sort_data(info, lambda x, y: x >= y)
        self.assertEqual(info, [5, 4, 3, 2, 1, 0])

        result = filter_data(data, lambda x: x % 2 == 0)
        self.assertEqual(result, [0, 2, 4])

        result = filter_data(data, lambda x: x % 2 == 1)
        self.assertEqual(result, [1, 3, 5])

        x1 = [1, 2, 3]
        x2 = [1, 2, 3]
        assert x1 == x2

        inf = Iterable()
        inf.append(1)
        inf.append(2)
        inf.append(3)
        it = iter(inf)
        self.assertEqual(next(it), 1)
        self.assertEqual(next(it), 2)
        self.assertEqual(next(it), 3)
        self.assertRaises(StopIteration, next, it)


if __name__ == "__main__":
    unittest.main()
