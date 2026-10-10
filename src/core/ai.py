"""Modular AI Engine Scaffolding.

This module provides scaffolding for pluggable AI algorithms, heuristics,
and minimax decision trees for Tic-Tac-Toe.
Currently, the runtime engine is directly served from logic.py.
"""

from typing import List, Optional


class BaseAI:
    """Base class for AI opponents."""

    def __init__(self, player: str = 'O'):
        self.player = player

    def get_move(self, board: List[Optional[str]], grid_size: int = 3) -> Optional[int]:
        """Compute the next move for this AI."""
        raise NotImplementedError("AI subclasses must implement get_move")
