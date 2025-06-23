"""
Unit tests for the calculator module.
"""

import unittest
from calculator import Calculator


class TestCalculator(unittest.TestCase):
    """Test cases for the Calculator class."""
    
    def setUp(self):
        """Set up test fixtures before each test method."""
        self.calc = Calculator()
    
    def test_add(self):
        """Test the add method."""
        self.assertEqual(self.calc.add(5, 3), 8)
        self.assertEqual(self.calc.add(-1, 1), 0)
        self.assertEqual(self.calc.add(-5, -3), -8)
        self.assertEqual(self.calc.add(0, 0), 0)
        self.assertEqual(self.calc.add(2.5, 3.7), 6.2)
    
    def test_subtract(self):
        """Test the subtract method."""
        self.assertEqual(self.calc.subtract(10, 4), 6)
        self.assertEqual(self.calc.subtract(5, 5), 0)
        self.assertEqual(self.calc.subtract(-3, -7), 4)
        self.assertEqual(self.calc.subtract(0, 5), -5)
        self.assertEqual(self.calc.subtract(7.5, 2.3), 5.2)
    
    def test_multiply(self):
        """Test the multiply method."""
        self.assertEqual(self.calc.multiply(6, 7), 42)
        self.assertEqual(self.calc.multiply(-3, 4), -12)
        self.assertEqual(self.calc.multiply(-2, -5), 10)
        self.assertEqual(self.calc.multiply(0, 100), 0)
        self.assertEqual(self.calc.multiply(2.5, 4), 10.0)
    
    def test_divide(self):
        """Test the divide method."""
        self.assertEqual(self.calc.divide(15, 3), 5)
        self.assertEqual(self.calc.divide(10, 2), 5)
        self.assertEqual(self.calc.divide(-12, 4), -3)
        self.assertEqual(self.calc.divide(-15, -3), 5)
        self.assertAlmostEqual(self.calc.divide(7, 3), 2.333333333333333)
    
    def test_divide_by_zero(self):
        """Test that dividing by zero raises ValueError."""
        with self.assertRaises(ValueError) as context:
            self.calc.divide(10, 0)
        self.assertEqual(str(context.exception), "Cannot divide by zero")
    
    def test_power(self):
        """Test the power method."""
        self.assertEqual(self.calc.power(2, 4), 16)
        self.assertEqual(self.calc.power(5, 0), 1)
        self.assertEqual(self.calc.power(3, 2), 9)
        self.assertEqual(self.calc.power(-2, 3), -8)
        self.assertEqual(self.calc.power(4, -1), 0.25)
    
    def test_square_root(self):
        """Test the square_root method."""
        self.assertEqual(self.calc.square_root(16), 4)
        self.assertEqual(self.calc.square_root(25), 5)
        self.assertEqual(self.calc.square_root(0), 0)
        self.assertEqual(self.calc.square_root(1), 1)
        self.assertAlmostEqual(self.calc.square_root(2), 1.4142135623730951)
    
    def test_square_root_negative(self):
        """Test that square root of negative number raises ValueError."""
        with self.assertRaises(ValueError) as context:
            self.calc.square_root(-4)
        self.assertEqual(str(context.exception), "Cannot calculate square root of negative number")
    
    def test_edge_cases(self):
        """Test edge cases and boundary conditions."""
        # Test with very large numbers
        self.assertEqual(self.calc.add(1e10, 1e10), 2e10)
        
        # Test with very small numbers
        self.assertAlmostEqual(self.calc.multiply(1e-10, 1e-10), 1e-20)
        
        # Test with floating point precision
        result = self.calc.add(0.1, 0.2)
        self.assertAlmostEqual(result, 0.3, places=10)


class TestCalculatorIntegration(unittest.TestCase):
    """Integration tests for calculator operations."""
    
    def setUp(self):
        """Set up test fixtures."""
        self.calc = Calculator()
    
    def test_complex_calculation(self):
        """Test a complex calculation using multiple operations."""
        # Calculate: ((5 + 3) * 2) / 4 - 1 = 3
        step1 = self.calc.add(5, 3)  # 8
        step2 = self.calc.multiply(step1, 2)  # 16
        step3 = self.calc.divide(step2, 4)  # 4
        result = self.calc.subtract(step3, 1)  # 3
        self.assertEqual(result, 3)
    
    def test_power_and_square_root(self):
        """Test that power and square root are inverse operations."""
        number = 9
        squared = self.calc.power(number, 2)
        sqrt_result = self.calc.square_root(squared)
        self.assertEqual(sqrt_result, number)


if __name__ == "__main__":
    # Run the tests with verbose output
    unittest.main(verbosity=2)
