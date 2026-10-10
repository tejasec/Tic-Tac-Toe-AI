"""Clock Mode (Coming Soon!).

In Clock Mode (Blitz Tic-Tac-Toe), each player operates under a countdown timer
(e.g., 3-5 seconds per turn, or a chess clock format). Failing to move before the
timer expires results in forfeiting the turn or losing the game.

TODO:
1. Implement turn timer timestamps and server-side move latency validation.
2. Add remaining_time fields to /api/action state responses.
3. Handle timeout forfeit conditions in check_game_over.
"""


def check_clock_expiration(turn_start_time, time_limit_seconds=5.0):
    """Stub to determine if a player's move timed out.

    TODO: Implement turn expiration verification.
    """
    raise NotImplementedError("Clock Mode is coming soon!")
