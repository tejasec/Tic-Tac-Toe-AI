"""Persistent Scoreboard and Stats Scaffolding.

This module provides scaffolding for storing match history, win rates,
and session scores across server restarts using sqlite3 or local JSON.

TODO:
1. Implement SQLite schema (table matches: id, mode, difficulty, winner, timestamp).
2. Provide load_scores() and save_match_result() functions.
3. Integrate into logic.py's TicTacToeLogic.end_game() hook.
"""

from typing import Dict


class ScoreStorage:
    """Stub interface for persistent score storage."""

    def __init__(self, db_path: str = "scores.db"):
        self.db_path = db_path

    def load_scores(self) -> Dict[str, int]:
        """Load stored stats.

        TODO: Connect to database/JSON file and query stats.
        """
        return {
            "pvp_x": 0, "pvp_o": 0, "pvp_ties": 0,
            "pva_x": 0, "pva_o": 0, "pva_ties": 0
        }

    def record_game(self, mode: str, winner: str):
        """Record game completion.

        TODO: Insert match record into database/JSON file.
        """
        pass
