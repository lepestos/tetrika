import unittest

from task1 import task


class MyTestCase(unittest.TestCase):
    def test_correctness(self):
        self.assertEqual(task('10'), 1)
        self.assertEqual(task('11110000'), 4)
        self.assertEqual(task('111100000'), 4)
        self.assertEqual(task('1111000000000000000'), 4)
        self.assertEqual(task('1111110000'), 6)
        self.assertEqual(task('111111111111111110000'), 17)
        self.assertEqual(task('111111111111111110000000000000000000000000000000000000000'), 17)
        self.assertEqual(task('111111111111111111111111111000000000'), 27)
        self.assertEqual(task('00000'), -1)
        self.assertEqual(task('111111111111'), -1)
        self.assertEqual(task(''), -1)


if __name__ == '__main__':
    unittest.main()
