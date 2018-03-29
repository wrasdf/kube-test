import unittest
# -*- coding: utf-8 -*-

class TestStringMethods(unittest.TestCase):

    def setUp(self):
        self.car = "New-Car"

    def test_isupper(self):
        self.assertEqual(self.car, "New-Car")

if __name__ == '__main__':
    unittest.main()
