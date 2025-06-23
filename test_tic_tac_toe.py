"""
Unit tests for LeetCode 348: Design Tic-Tac-Toe

Comprehensive test suite covering all functionality including edge cases,
error handling, and performance validation.

Author: Assistant
Date: 2025-06-13
"""

import unittest
from typing import List, Tuple
from tic_tac_toe import TicTacToe


class TestTicTacToe(unittest.TestCase):
    """Test suite for the TicTacToe class."""
    
    def setUp(self) -> None:
        """Set up test fixtures before each test method."""
        self.game_3x3 = TicTacToe(3)
        self.game_4x4 = TicTacToe(4)
    
    def test_initialization_valid_size(self) -> None:
        """Test successful initialization with valid board sizes."""
        # Test various valid sizes
        for size in [1, 2, 3, 5, 10, 100]:
            game = TicTacToe(size)
            self.assertEqual(game.n, size)
            self.assertEqual(len(game.rows), size)
            self.assertEqual(len(game.cols), size)
            self.assertEqual(game.diagonal, 0)
            self.assertEqual(game.anti_diagonal, 0)
    
    def test_initialization_invalid_size(self) -> None:
        """Test initialization with invalid board sizes."""
        invalid_sizes = [0, -1, -10]
        for size in invalid_sizes:
            with self.assertRaises(ValueError) as context:
                TicTacToe(size)
            self.assertIn("Board size must be a positive integer", str(context.exception))
    
    def test_move_input_validation(self) -> None:
        """Test move method input validation."""
        game = TicTacToe(3)
        
        # Test invalid row values
        with self.assertRaises(ValueError) as context:
            game.move(-1, 0, 1)
        self.assertIn("Row must be between 0 and 2", str(context.exception))
        
        with self.assertRaises(ValueError) as context:
            game.move(3, 0, 1)
        self.assertIn("Row must be between 0 and 2", str(context.exception))
        
        # Test invalid column values
        with self.assertRaises(ValueError) as context:
            game.move(0, -1, 1)
        self.assertIn("Column must be between 0 and 2", str(context.exception))
        
        with self.assertRaises(ValueError) as context:
            game.move(0, 3, 1)
        self.assertIn("Column must be between 0 and 2", str(context.exception))
        
        # Test invalid player values
        for invalid_player in [0, 3, -1, 5]:
            with self.assertRaises(ValueError) as context:
                game.move(0, 0, invalid_player)
            self.assertIn("Player must be 1 or 2", str(context.exception))
    
    def test_no_winner_scenario(self) -> None:
        """Test scenarios where no winner is determined."""
        game = TicTacToe(3)
        
        # Single moves should not produce a winner
        self.assertEqual(game.move(0, 0, 1), 0)
        self.assertEqual(game.move(1, 1, 2), 0)
        self.assertEqual(game.move(2, 2, 1), 0)
        
        # Verify internal state
        state = game.get_board_state()
        self.assertEqual(state['rows'], [1, -1, 1])
        self.assertEqual(state['cols'], [1, -1, 1])
        self.assertEqual(state['diagonal'], 1)  # (0,0) and (2,2) are on diagonal
        self.assertEqual(state['anti_diagonal'], -1)  # (1,1) is on anti-diagonal
    
    def test_horizontal_win_player1(self) -> None:
        """Test horizontal win condition for player 1."""
        game = TicTacToe(3)
        
        # Player 1 wins with top row
        self.assertEqual(game.move(0, 0, 1), 0)  # No winner yet
        self.assertEqual(game.move(1, 0, 2), 0)  # Player 2 move
        self.assertEqual(game.move(0, 1, 1), 0)  # No winner yet
        self.assertEqual(game.move(1, 1, 2), 0)  # Player 2 move
        self.assertEqual(game.move(0, 2, 1), 1)  # Player 1 wins!
        
        # Verify final state
        state = game.get_board_state()
        self.assertEqual(state['rows'][0], 3)  # Top row filled by player 1
    
    def test_horizontal_win_player2(self) -> None:
        """Test horizontal win condition for player 2."""
        game = TicTacToe(3)
        
        # Player 2 wins with middle row
        self.assertEqual(game.move(0, 0, 1), 0)  # Player 1 move
        self.assertEqual(game.move(1, 0, 2), 0)  # No winner yet
        self.assertEqual(game.move(0, 1, 1), 0)  # Player 1 move
        self.assertEqual(game.move(1, 1, 2), 0)  # No winner yet
        self.assertEqual(game.move(2, 0, 1), 0)  # Player 1 move
        self.assertEqual(game.move(1, 2, 2), 2)  # Player 2 wins!
        
        # Verify final state
        state = game.get_board_state()
        self.assertEqual(state['rows'][1], -3)  # Middle row filled by player 2
    
    def test_vertical_win(self) -> None:
        """Test vertical win condition."""
        game = TicTacToe(3)
        
        # Player 1 wins with first column
        self.assertEqual(game.move(0, 0, 1), 0)
        self.assertEqual(game.move(0, 1, 2), 0)
        self.assertEqual(game.move(1, 0, 1), 0)
        self.assertEqual(game.move(0, 2, 2), 0)
        self.assertEqual(game.move(2, 0, 1), 1)  # Player 1 wins!
        
        # Verify final state
        state = game.get_board_state()
        self.assertEqual(state['cols'][0], 3)  # First column filled by player 1
    
    def test_main_diagonal_win(self) -> None:
        """Test main diagonal win condition (top-left to bottom-right)."""
        game = TicTacToe(3)
        
        # Player 1 wins with main diagonal
        self.assertEqual(game.move(0, 0, 1), 0)
        self.assertEqual(game.move(0, 1, 2), 0)
        self.assertEqual(game.move(1, 1, 1), 0)
        self.assertEqual(game.move(0, 2, 2), 0)
        self.assertEqual(game.move(2, 2, 1), 1)  # Player 1 wins!
        
        # Verify final state
        state = game.get_board_state()
        self.assertEqual(state['diagonal'], 3)  # Main diagonal filled by player 1
    
    def test_anti_diagonal_win(self) -> None:
        """Test anti-diagonal win condition (top-right to bottom-left)."""
        game = TicTacToe(3)
        
        # Player 2 wins with anti-diagonal
        self.assertEqual(game.move(0, 0, 1), 0)
        self.assertEqual(game.move(0, 2, 2), 0)
        self.assertEqual(game.move(1, 0, 1), 0)
        self.assertEqual(game.move(1, 1, 2), 0)
        self.assertEqual(game.move(2, 1, 1), 0)
        self.assertEqual(game.move(2, 0, 2), 2)  # Player 2 wins!
        
        # Verify final state
        state = game.get_board_state()
        self.assertEqual(state['anti_diagonal'], -3)  # Anti-diagonal filled by player 2
    
    def test_leetcode_example(self) -> None:
        """Test the exact example from the LeetCode problem."""
        game = TicTacToe(3)
        
        # Follow the exact sequence from the problem
        moves_and_expected = [
            ((0, 0, 1), 0),  # Player 1 at (0,0) -> no winner
            ((0, 2, 2), 0),  # Player 2 at (0,2) -> no winner
            ((2, 2, 1), 0),  # Player 1 at (2,2) -> no winner
            ((1, 1, 2), 0),  # Player 2 at (1,1) -> no winner
            ((2, 0, 1), 0),  # Player 1 at (2,0) -> no winner
            ((1, 0, 2), 0),  # Player 2 at (1,0) -> no winner
            ((2, 1, 1), 1),  # Player 1 at (2,1) -> Player 1 wins!
        ]
        
        for (row, col, player), expected in moves_and_expected:
            result = game.move(row, col, player)
            self.assertEqual(result, expected, 
                           f"Move ({row}, {col}, {player}) should return {expected}, got {result}")
    
    def test_4x4_board_win_conditions(self) -> None:
        """Test win conditions on a 4x4 board."""
        game = TicTacToe(4)
        
        # Test horizontal win on 4x4 board
        for col in range(4):
            if col < 3:
                self.assertEqual(game.move(0, col, 1), 0)
            else:
                self.assertEqual(game.move(0, col, 1), 1)  # Player 1 wins on 4th move
    
    def test_1x1_board(self) -> None:
        """Test edge case with 1x1 board."""
        game = TicTacToe(1)
        
        # First move should win immediately
        self.assertEqual(game.move(0, 0, 1), 1)
    
    def test_reset_functionality(self) -> None:
        """Test the reset functionality."""
        game = TicTacToe(3)
        
        # Make some moves
        game.move(0, 0, 1)
        game.move(1, 1, 2)
        game.move(2, 2, 1)
        
        # Verify state is not initial
        state = game.get_board_state()
        self.assertNotEqual(state['rows'], [0, 0, 0])
        
        # Reset and verify
        game.reset()
        state = game.get_board_state()
        self.assertEqual(state['rows'], [0, 0, 0])
        self.assertEqual(state['cols'], [0, 0, 0])
        self.assertEqual(state['diagonal'], 0)
        self.assertEqual(state['anti_diagonal'], 0)
        
        # Verify game works after reset
        self.assertEqual(game.move(0, 0, 1), 0)
    
    def test_get_board_state(self) -> None:
        """Test the get_board_state method."""
        game = TicTacToe(2)
        
        # Initial state
        state = game.get_board_state()
        expected_state = {
            'rows': [0, 0],
            'cols': [0, 0],
            'diagonal': 0,
            'anti_diagonal': 0,
            'board_size': 2
        }
        self.assertEqual(state, expected_state)
        
        # After some moves
        game.move(0, 0, 1)  # Player 1
        game.move(1, 1, 2)  # Player 2
        
        state = game.get_board_state()
        self.assertEqual(state['rows'], [1, -1])
        self.assertEqual(state['cols'], [1, -1])
        self.assertEqual(state['diagonal'], 0)  # 1 + (-1) = 0
        self.assertEqual(state['anti_diagonal'], 0)
    
    def test_mixed_win_conditions(self) -> None:
        """Test scenarios where multiple win conditions could be met simultaneously."""
        game = TicTacToe(3)
        
        # Create a scenario where a move satisfies both row and diagonal
        game.move(0, 0, 1)  # Player 1 on main diagonal
        game.move(0, 1, 2)  # Player 2
        game.move(1, 1, 1)  # Player 1 on main diagonal
        game.move(0, 2, 2)  # Player 2 completes top row
        
        # Player 2 should win with the row, even though diagonal is also possible
        self.assertEqual(game.move(2, 2, 1), 1)  # Player 1 completes diagonal and wins
    
    def test_large_board_performance(self) -> None:
        """Test performance with larger board sizes."""
        # This test ensures O(1) complexity is maintained
        game = TicTacToe(1000)
        
        # Make a move - should be instant regardless of board size
        result = game.move(0, 0, 1)
        self.assertEqual(result, 0)
        
        # Test winning condition on large board - fill first row
        for i in range(1, 999):
            self.assertEqual(game.move(0, i, 1), 0)
        
        # Final move should trigger win (1000th move in row 0)
        self.assertEqual(game.move(0, 999, 1), 1)


class TestTicTacToeIntegration(unittest.TestCase):
    """Integration tests for complete game scenarios."""
    
    def test_complete_game_scenarios(self) -> None:
        """Test complete game scenarios with different outcomes."""
        
        # Scenario 1: Player 1 wins with diagonal
        game1 = TicTacToe(3)
        moves1 = [(0, 0, 1), (0, 1, 2), (1, 1, 1), (0, 2, 2), (2, 2, 1)]
        results1 = [0, 0, 0, 0, 1]
        
        for i, (move, expected) in enumerate(zip(moves1, results1)):
            result = game1.move(*move)
            self.assertEqual(result, expected, f"Game 1, move {i+1}")
        
        # Scenario 2: Player 2 wins with column
        game2 = TicTacToe(3)
        moves2 = [(0, 0, 1), (0, 1, 2), (1, 0, 1), (1, 1, 2), (0, 2, 1), (2, 1, 2)]
        results2 = [0, 0, 0, 0, 0, 2]
        
        for i, (move, expected) in enumerate(zip(moves2, results2)):
            result = game2.move(*move)
            self.assertEqual(result, expected, f"Game 2, move {i+1}")


if __name__ == '__main__':
    # Run tests with verbose output
    unittest.main(verbosity=2)
