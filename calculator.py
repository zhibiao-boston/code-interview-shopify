"""
A simple calculator module with basic arithmetic operations.
"""

class Calculator:
    """A calculator class that performs basic arithmetic operations."""
    
    def add(self, a, b):
        """Add two numbers and return the result."""
        return a + b
    
    def subtract(self, a, b):
        """Subtract b from a and return the result."""
        return a - b
    
    def multiply(self, a, b):
        """Multiply two numbers and return the result."""
        return a * b
    
    def divide(self, a, b):
        """Divide a by b and return the result."""
        if b == 0:
            raise ValueError("Cannot divide by zero")
        return a / b
    
    def power(self, base, exponent):
        """Raise base to the power of exponent."""
        return base ** exponent
    
    def square_root(self, number):
        """Calculate the square root of a number."""
        if number < 0:
            raise ValueError("Cannot calculate square root of negative number")
        return number ** 0.5


def main():
    """Example usage of the Calculator class."""
    calc = Calculator()
    
    print("Calculator Example:")
    print(f"5 + 3 = {calc.add(5, 3)}")
    print(f"10 - 4 = {calc.subtract(10, 4)}")
    print(f"6 * 7 = {calc.multiply(6, 7)}")
    print(f"15 / 3 = {calc.divide(15, 3)}")
    print(f"2 ^ 4 = {calc.power(2, 4)}")
    print(f"√16 = {calc.square_root(16)}")


if __name__ == "__main__":
    main()
