import unittest

a = {'key1': 5, 'key2': 7}
b = {'key1': 6, 'key2': 7, 'key3': 9}

class Test1(unittest.TestCase):
    def test_1(self):
        self.assertDictEqual(a, b)

unittest.main()