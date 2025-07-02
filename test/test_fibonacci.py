"""
Unit tests for the Fibonacci class.
"""

import unittest
import sys
import os

# Add the script directory to the path so we can import the Fibonacci class
sys.path.insert(0, os.path.join(os.path.dirname(__file__), '..', 'script'))

from fibonacci import Fibonacci


class TestFibonacci(unittest.TestCase):
    """Test cases for the Fibonacci class."""
    
    def setUp(self):
        """Set up test fixtures before each test method."""
        self.fib = Fibonacci()
    
    def test_nth_fibonacci_iterative_basic_cases(self):
        """Test basic Fibonacci calculations using iterative method."""
        # Test known Fibonacci values
        test_cases = [
            (0, 0),
            (1, 1),
            (2, 1),
            (3, 2),
            (4, 3),
            (5, 5),
            (6, 8),
            (7, 13),
            (8, 21),
            (9, 34),
            (10, 55)
        ]
        
        for n, expected in test_cases:
            with self.subTest(n=n):
                self.assertEqual(self.fib.nth_fibonacci_iterative(n), expected)
    
    def test_nth_fibonacci_recursive_basic_cases(self):
        """Test basic Fibonacci calculations using recursive method."""
        # Test known Fibonacci values
        test_cases = [
            (0, 0),
            (1, 1),
            (2, 1),
            (3, 2),
            (4, 3),
            (5, 5),
            (6, 8),
            (7, 13),
            (8, 21),
            (9, 34),
            (10, 55)
        ]
        
        for n, expected in test_cases:
            with self.subTest(n=n):
                self.assertEqual(self.fib.nth_fibonacci_recursive(n), expected)
    
    def test_iterative_vs_recursive_consistency(self):
        """Test that iterative and recursive methods produce the same results."""
        for n in range(15):
            with self.subTest(n=n):
                iterative_result = self.fib.nth_fibonacci_iterative(n)
                recursive_result = self.fib.nth_fibonacci_recursive(n)
                self.assertEqual(iterative_result, recursive_result)
    
    def test_nth_fibonacci_negative_input(self):
        """Test that negative inputs raise ValueError."""
        with self.assertRaises(ValueError):
            self.fib.nth_fibonacci_iterative(-1)
        
        with self.assertRaises(ValueError):
            self.fib.nth_fibonacci_recursive(-1)
    
    def test_nth_fibonacci_invalid_type(self):
        """Test that non-integer inputs raise TypeError."""
        invalid_inputs = [3.14, "5", None, [5], {"n": 5}]
        
        for invalid_input in invalid_inputs:
            with self.subTest(input=invalid_input):
                with self.assertRaises(TypeError):
                    self.fib.nth_fibonacci_iterative(invalid_input)
                
                with self.assertRaises(TypeError):
                    self.fib.nth_fibonacci_recursive(invalid_input)
    
    def test_generate_sequence_basic(self):
        """Test basic sequence generation."""
        test_cases = [
            (0, []),
            (1, [0]),
            (2, [0, 1]),
            (5, [0, 1, 1, 2, 3]),
            (10, [0, 1, 1, 2, 3, 5, 8, 13, 21, 34])
        ]
        
        for count, expected in test_cases:
            with self.subTest(count=count):
                self.assertEqual(self.fib.generate_sequence(count), expected)
    
    def test_generate_sequence_negative_count(self):
        """Test that negative count raises ValueError."""
        with self.assertRaises(ValueError):
            self.fib.generate_sequence(-1)
    
    def test_generate_sequence_invalid_type(self):
        """Test that non-integer count raises TypeError."""
        invalid_inputs = [3.14, "5", None, [5]]
        
        for invalid_input in invalid_inputs:
            with self.subTest(input=invalid_input):
                with self.assertRaises(TypeError):
                    self.fib.generate_sequence(invalid_input)
    
    def test_is_fibonacci_number_positive_cases(self):
        """Test is_fibonacci_number with valid Fibonacci numbers."""
        fibonacci_numbers = [0, 1, 2, 3, 5, 8, 13, 21, 34, 55, 89, 144]
        
        for num in fibonacci_numbers:
            with self.subTest(num=num):
                self.assertTrue(self.fib.is_fibonacci_number(num))
    
    def test_is_fibonacci_number_negative_cases(self):
        """Test is_fibonacci_number with non-Fibonacci numbers."""
        non_fibonacci_numbers = [4, 6, 7, 9, 10, 11, 12, 14, 15, 16, 17, 18, 19, 20, 22]
        
        for num in non_fibonacci_numbers:
            with self.subTest(num=num):
                self.assertFalse(self.fib.is_fibonacci_number(num))
    
    def test_is_fibonacci_number_negative_input(self):
        """Test is_fibonacci_number with negative numbers."""
        self.assertFalse(self.fib.is_fibonacci_number(-1))
        self.assertFalse(self.fib.is_fibonacci_number(-5))
    
    def test_is_fibonacci_number_invalid_type(self):
        """Test is_fibonacci_number with invalid input types."""
        invalid_inputs = [3.14, "5", None, [5]]
        
        for invalid_input in invalid_inputs:
            with self.subTest(input=invalid_input):
                with self.assertRaises(TypeError):
                    self.fib.is_fibonacci_number(invalid_input)
    
    def test_cache_functionality(self):
        """Test that the cache works correctly for recursive method."""
        # Clear cache and calculate a number
        self.fib.clear_cache()
        result1 = self.fib.nth_fibonacci_recursive(10)
        
        # The cache should now contain values up to 10
        self.assertIn(10, self.fib._cache)
        self.assertEqual(self.fib._cache[10], 55)
        
        # Calculate the same number again (should use cache)
        result2 = self.fib.nth_fibonacci_recursive(10)
        self.assertEqual(result1, result2)
    
    def test_clear_cache(self):
        """Test cache clearing functionality."""
        # Add some values to cache
        self.fib.nth_fibonacci_recursive(5)
        self.assertIn(5, self.fib._cache)
        
        # Clear cache
        self.fib.clear_cache()
        
        # Cache should only contain base cases
        expected_cache = {0: 0, 1: 1}
        self.assertEqual(self.fib._cache, expected_cache)
    
    def test_large_fibonacci_numbers(self):
        """Test calculation of larger Fibonacci numbers."""
        # Test a moderately large Fibonacci number
        n = 20
        expected = 6765  # 20th Fibonacci number
        
        self.assertEqual(self.fib.nth_fibonacci_iterative(n), expected)
        self.assertEqual(self.fib.nth_fibonacci_recursive(n), expected)
    
    def test_sequence_length_consistency(self):
        """Test that generated sequences have the correct length."""
        for count in range(0, 20):
            with self.subTest(count=count):
                sequence = self.fib.generate_sequence(count)
                self.assertEqual(len(sequence), count)


class TestFibonacciPerformance(unittest.TestCase):
    """Performance-related tests for the Fibonacci class."""
    
    def setUp(self):
        """Set up test fixtures."""
        self.fib = Fibonacci()
    
    def test_iterative_performance(self):
        """Test that iterative method can handle reasonably large numbers."""
        # This should complete quickly
        result = self.fib.nth_fibonacci_iterative(100)
        self.assertIsInstance(result, int)
        self.assertGreater(result, 0)
    
    def test_recursive_with_memoization_performance(self):
        """Test that recursive method with memoization performs well."""
        # This should complete quickly due to memoization
        result = self.fib.nth_fibonacci_recursive(100)
        self.assertIsInstance(result, int)
        self.assertGreater(result, 0)


if __name__ == '__main__':
    # Run the tests
    unittest.main(verbosity=2)
