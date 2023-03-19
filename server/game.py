from enum import Enum
from datetime import datetime
from typing import Optional
import uuid
import json


class GameRoom:
    def __init__(self):
        self._id = uuid.uuid4()
        self._running = True
        self._max_lightning = 3
        self._players: list[Player] = []
        self._admin = Optional[Player]

    @property
    def id(self):
        return str(self._id)

    @property
    def players(self):
        return self._players

    @property
    def admin(self) -> bool:
        return self._admin

    def add_player(self, player_name: str):
        player = Player(player_name)
        if self.players == []:
            self._admin = player
        self.players.append(Player(player_name))

    def get_lobby_json(self) -> dict[str, any]:
        return json.dumps({
            "player_list": [player.name for player in self.players],
            "running": self._running,
            "admin": self.admin.name
        })


class Team(Enum):
    GOOD = 1
    BAD = 2


class Player:
    def __init__(self, name: str, is_admin=False):
        self.name = name
        self.life = 3
        # TODO: make character to enum instead of str
        self.character: str = Optional[str]
        self.is_admin = is_admin
        self.team = Optional[Team]
        self.lastAction: datetime = datetime.now()
        self.hold_dice = False


