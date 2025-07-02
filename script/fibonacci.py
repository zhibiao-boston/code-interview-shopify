"""
Fibonacci class implementation with multiple calculation methods.
"""


class Fibonacci:
    """
    A class to handle Fibonacci number calculations and sequence generation.
    
    The Fibonacci sequence is defined as:
    F(0) = 0, F(1) = 1, F(n) = F(n-1) + F(n-2) for n > 1
    """
    
    def __init__(self):
        """Initialize the Fibonacci class."""
        self._cache = {0: 0, 1: 1}
    
    def nth_fibonacci_iterative(self, n):
        """
        Calculate the nth Fibonacci number using iterative approach.
        
        Args:
            n (int): The position in the Fibonacci sequence (0-indexed)
            
        Returns:
            int: The nth Fibonacci number
            
        Raises:
            ValueError: If n is negative
            TypeError: If n is not an integer
        """
        if not isinstance(n, int):
            raise TypeError("Input must be an integer")
        
        if n < 0:
            raise ValueError("Input must be non-negative")
        
        if n <= 1:
            return n
        
        a, b = 0, 1
        for _ in range(2, n + 1):
            a, b = b, a + b
        
        return b
    
    def nth_fibonacci_recursive(self, n):
        """
        Calculate the nth Fibonacci number using recursive approach with memoization.
        
        Args:
            n (int): The position in the Fibonacci sequence (0-indexed)
            
        Returns:
            int: The nth Fibonacci number
            
        Raises:
            ValueError: If n is negative
            TypeError: If n is not an integer
        """
        if not isinstance(n, int):
            raise TypeError("Input must be an integer")
        
        if n < 0:
            raise ValueError("Input must be non-negative")
        
        if n in self._cache:
            return self._cache[n]
        
        self._cache[n] = self.nth_fibonacci_recursive(n - 1) + self.nth_fibonacci_recursive(n - 2)
        return self._cache[n]
    
    def generate_sequence(self, count):
        """
        Generate a Fibonacci sequence with the specified number of terms.
        
        Args:
            count (int): Number of Fibonacci numbers to generate
            
        Returns:
            list: List of Fibonacci numbers
            
        Raises:
            ValueError: If count is negative
            TypeError: If count is not an integer
        """
        if not isinstance(count, int):
            raise TypeError("Count must be an integer")
        
        if count < 0:
            raise ValueError("Count must be non-negative")
        
        if count == 0:
            return []
        
        sequence = []
        for i in range(count):
            sequence.append(self.nth_fibonacci_iterative(i))
        
        return sequence
    
    def is_fibonacci_number(self, num):
        """
        Check if a given number is a Fibonacci number.
        
        Args:
            num (int): The number to check
            
        Returns:
            bool: True if the number is a Fibonacci number, False otherwise
            
        Raises:
            TypeError: If num is not an integer
        """
        if not isinstance(num, int):
            raise TypeError("Input must be an integer")
        
        if num < 0:
            return False
        
        # Generate Fibonacci numbers until we reach or exceed the target
        a, b = 0, 1
        while a < num:
            a, b = b, a + b
        
        return a == num
    
    def clear_cache(self):
        """Clear the memoization cache."""
        self._cache = {0: 0, 1: 1}


if __name__ == "__main__":
    # Example usage
    fib = Fibonacci()
    
    print("First 10 Fibonacci numbers:")
    print(fib.generate_sequence(10))
    
    print(f"\n10th Fibonacci number (iterative): {fib.nth_fibonacci_iterative(10)}")
    print(f"10th Fibonacci number (recursive): {fib.nth_fibonacci_recursive(10)}")
    
    print(f"\nIs 21 a Fibonacci number? {fib.is_fibonacci_number(21)}")
    print(f"Is 22 a Fibonacci number? {fib.is_fibonacci_number(22)}")
