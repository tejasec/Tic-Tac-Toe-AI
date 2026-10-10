"""Decay Mode (Coming Soon!).

In Decay Mode (Infinite / Sliding-Window Tic-Tac-Toe), each player can only keep
a maximum number of marks on the board at a time (e.g. 3 marks max). Placing a 4th
mark causes the player's oldest mark to fade/decay and be cleared.

TODO:
1. Maintain an ordered queue of move indices per player: move_history[player].
2. Expire the oldest piece when len(player_moves) > max_marks.
3. Add visual fading indicators to UI for decaying pieces.
"""


def apply_decay(board, player_move_queue, max_marks=3):
    """Stub to remove oldest player mark when exceeding max_marks.

    TODO: Implement FIFO piece expiration.
    """
    raise NotImplementedError("Decay Mode is coming soon!")
