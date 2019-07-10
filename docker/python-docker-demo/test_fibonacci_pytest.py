"""
Tests for Fibonacci number function
"""
from fibonacci import compute_fib
import pytest
import unittest
import xmlrunner

class TestFibonaaci(unittest.TestCase):

    def test_compute_small_fib(self):
        self.assertEqual(compute_fib(7), 13)

    def test_compute_large_fib(self):
        self.assertEqual(compute_fib(20), 6765)

    def test_invalid_int_arg(self):
        with self.assertRaises(ValueError):
            compute_fib(-1)

if __name__ == '__main__':
    unittest.main(
        testRunner=xmlrunner.XMLTestRunner(output='test-reports'),
        # these make sure that some options that are not applicable
        # remain hidden from the help menu
        failfast=False, buffer=False, catchbreak=False
    )



