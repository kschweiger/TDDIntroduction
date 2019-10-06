import unittest


class TestSum(unittest.TestCase):
    def test_sum(self):
        res = sum([2, 4, 6])
        self.assertEqual(res, 12)

    def test_sum_fail_str(self):
        with self.assertRaises(TypeError):
            res = sum("SOMESTRING")
