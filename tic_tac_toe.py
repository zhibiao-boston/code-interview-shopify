"""
LeetCode 348: Design Tic-Tac-Toe

Design a Tic-tac-toe game that is played between two players on an n x n grid.
Optimized solution with O(1) time complexity per move and O(n) space complexity.

Author: Assistant
Date: 2025-06-13
"""

from typing import Optional


class TicTacToe:
    """
    A Tic-Tac-Toe game implementation optimized for O(1) move operations.
    
    This implementation uses a space-time trade-off to achieve constant time
    complexity per move by tracking the sum of moves in each row, column,
    and diagonal instead of maintaining the entire board state.
    
    Attributes:
        n (int): The size of the n x n game board
        rows (list[int]): Sum of moves for each row
        cols (list[int]): Sum of moves for each column  
        diagonal (int): Sum of moves on the main diagonal (top-left to bottom-right)
        anti_diagonal (int): Sum of moves on the anti-diagonal (top-right to bottom-left)
    """
    
    def __init__(self, n: int) -> None:
        """
        Initialize the Tic-Tac-Toe game with an n x n board.
        
        Args:
            n (int): The size of the board (must be positive)
            
        Raises:
            ValueError: If n is not a positive integer
        """
        if n <= 0:
            raise ValueError("Board size must be a positive integer")
            
        self.n = n
        self.rows = [0] * n
        self.cols = [0] * n
        self.diagonal = 0
        self.anti_diagonal = 0
    
    def move(self, row: int, col: int, player: int) -> int:
        """
        Make a move on the board and check for a winner.
        
        The scoring system:
        - Player 1: adds +1 to the corresponding row, column, and diagonals
        - Player 2: adds -1 to the corresponding row, column, and diagonals
        
        A player wins when the absolute value of any row, column, or diagonal
        sum equals n (the board size).
        
        Args:
            row (int): The row index (0-indexed)
            col (int): The column index (0-indexed)
            player (int): The player number (1 or 2)
            
        Returns:
            int: 0 if no winner, otherwise the winning player number (1 or 2)
            
        Raises:
            ValueError: If row, col, or player values are invalid
        """
        # Validate input parameters
        if not (0 <= row < self.n):
            raise ValueError(f"Row must be between 0 and {self.n - 1}")
        if not (0 <= col < self.n):
            raise ValueError(f"Column must be between 0 and {self.n - 1}")
        if player not in (1, 2):
            raise ValueError("Player must be 1 or 2")
        
        # Determine the move value: +1 for player 1, -1 for player 2
        move_value = 1 if player == 1 else -1
        
        # Update row and column sums
        self.rows[row] += move_value
        self.cols[col] += move_value
        
        # Update diagonal sums if the move is on a diagonal
        if row == col:
            self.diagonal += move_value
            
        if row + col == self.n - 1:
            self.anti_diagonal += move_value
        
        # Check for winning condition
        if (abs(self.rows[row]) == self.n or 
            abs(self.cols[col]) == self.n or 
            abs(self.diagonal) == self.n or 
            abs(self.anti_diagonal) == self.n):
            return player
            
        return 0
    
    def get_board_state(self) -> dict:
        """
        Get the current internal state of the game for debugging purposes.
        
        Returns:
            dict: A dictionary containing the current state of all tracking arrays
        """
        return {
            'rows': self.rows.copy(),
            'cols': self.cols.copy(),
            'diagonal': self.diagonal,
            'anti_diagonal': self.anti_diagonal,
            'board_size': self.n
        }
    
    def reset(self) -> None:
        """
        Reset the game to initial state.
        """
        self.rows = [0] * self.n
        self.cols = [0] * self.n
        self.diagonal = 0
        self.anti_diagonal = 0


# Example usage and demonstration
if __name__ == "__main__":
    # Create a 3x3 Tic-Tac-Toe game
    game = TicTacToe(3)
    
    # Simulate the example from the problem
    moves = [
        (0, 0, 1),  # Player 1 at (0,0)
        (0, 2, 2),  # Player 2 at (0,2)
        (2, 2, 1),  # Player 1 at (2,2)
        (1, 1, 2),  # Player 2 at (1,1)
        (2, 0, 1),  # Player 1 at (2,0)
        (1, 0, 2),  # Player 2 at (1,0)
        (2, 1, 1),  # Player 1 at (2,1) - should win
    ]
    
    print("Tic-Tac-Toe Game Simulation:")
    print("=" * 30)
    
    for i, (row, col, player) in enumerate(moves):
        result = game.move(row, col, player)
        print(f"Move {i + 1}: Player {player} at ({row}, {col}) -> Result: {result}")
        if result != 0:
            print(f"🎉 Player {result} wins!")
            break
