"""Modular Core Game Logic Scaffolding.

This module provides scaffolding for future object-oriented decomposition
of the Tic-Tac-Toe game engine, supporting arbitrary grid sizes and custom rules.
Currently, the runtime engine is directly served from logic.py.
"""

PLAYER_X = 'X'
PLAYER_O = 'O'


class Board:
    """Represents a generalized N x N game board."""

    def __init__(self, size: int = 3):
        self.size = size
        self.cells = [None] * (size * size)

    def is_valid_move(self, index: int) -> bool:
        """Check whether index is in range and unoccupied."""
        return 0 <= index < len(self.cells) and self.cells[index] is None

    def make_move(self, index: int, player: str) -> bool:
        """Place mark if legal."""
        if self.is_valid_move(index):
            self.cells[index] = player
            return True
        return False

    def available_moves(self) -> list:
        """Return indices of empty cells."""
        return [i for i, val in enumerate(self.cells) if val is None]

    def reset(self):
        """Reset board to empty."""
        self.cells = [None] * (self.size * self.size)
