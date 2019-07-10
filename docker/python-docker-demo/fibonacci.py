"""
Calculates a desired Fibonacci number. A Fibonacci number is defined by the
following recurrence relation: F(n) = F(n-1) + F(n-2), F(0) = 0, F(1) = 1.
For example, the first 5 Fibonacci numbers are 1, 1, 2, 3, 5.
"""
import pytest

def compute_fib(num):
    """
    Computes the (num)th Fibonacci number
    :param num: the (num)th Fibonacci number (integer) to compute
    :return: the (num)th Fibonacci number
    """
    if num <= 0:
        raise ValueError("Not a positive integer")
    fib2 = 0
    fib1 = 1
    fib_num = 1 # The (num)th Fibonacci number
    index = 1
    while index < num:
        fib_num = fib1 + fib2
        fib2 = fib1
        fib1 = fib_num
        index += 1
    return fib_num