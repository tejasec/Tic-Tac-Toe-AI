"""Online Multiplayer Networking Scaffolding.

This module provides scaffolding for remote two-player rooms, matchmaking,
and real-time move synchronization.

TODO:
1. Implement RoomManager for session/lobby creation with 6-character room codes.
2. Provide WebSockets or SSE/Long-polling endpoints for real-time moves.
3. Integrate player disconnect timeouts and reconnect mechanisms.
"""

from typing import Dict, Optional


class Room:
    """Represents a networked game lobby for 2 remote players."""

    def __init__(self, room_id: str):
        self.room_id = room_id
        self.player_x_id: Optional[str] = None
        self.player_o_id: Optional[str] = None
        self.board_state = []
        self.is_started = False


class RoomManager:
    """Manages active multiplayer rooms."""

    def __init__(self):
        self.rooms: Dict[str, Room] = {}

    def create_room(self, host_player_id: str) -> str:
        """Create new room and return room code.

        TODO: Generate unique code, store Room instance.
        """
        raise NotImplementedError("Online Multiplayer is coming soon!")

    def join_room(self, room_id: str, client_player_id: str) -> bool:
        """Join existing room.

        TODO: Assign player to Room, notify host.
        """
        raise NotImplementedError("Online Multiplayer is coming soon!")
