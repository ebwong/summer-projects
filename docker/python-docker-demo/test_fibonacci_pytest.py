"""
Tests for Fibonacci number function
"""
from fibonacci import compute_fib
import pytest

def test_compute_small_fib():
    assert compute_fib(7) == 13
    print("Test 'test_compute_small_fib' complete")

def test_compute_large_fib():
    assert compute_fib(20) == 6765
    print("Test 'test_compute_large_fib' complete")


def test_invalid_int_arg():
    with pytest.raises(ValueError):
        compute_fib(-1)
        print("Test 'test_invalid_int_arg' complete")

