from enum import Enum, IntEnum
from datetime import datetime
from typing import Optional, Self
from dataclasses import dataclass
import random
import uuid
import json


class GameState(IntEnum):
    LOBBY = 1
    STARTED = 2


class Team(Enum):
    GOOD = 1
    EVIL = 2


class Role(Enum):
    HACKER = 1
    MARINE = 2
    COMMUNICATIONS_OFFICER = 3
    TECHNICIAN = 4
    AUGMENTED = 5
    CAPTAIN = 6
    SECURITY_OFFICER = 7
    DOCTOR = 8
    PERSONAL_OFFICER = 9
    MANUAL_LABORER = 10
    PILOT = 11
    ENGINEER = 12


@dataclass
class Player:
    def __init__(self, name: str, is_admin=False):
        self.name = name
        self.helth = 2
        self.is_admin = is_admin
        self.role: Optional[Role]
        self.team = Optional[Team]
        self.lastAction: datetime = datetime.now()
        self.hold_dice = False
        self.is_infected = False

    def set_team(self, team: Team) -> Self:
        self.team = team
        return self

    def set_role(self, role: Role) -> Self:
        self.role = role
        return self

    def set_infected(self, is_infected) -> Self:
        self.is_infected = is_infected
        return self


class GameRoom:
    def __init__(self, id:str):
        self._id = id
        self._running = True
        self._max_lightning = 3
        self._players: list[Player] = []
        self._admin: Player
        self._state = GameState.LOBBY

    @property
    def id(self):
        return str(self._id)

    @property
    def players(self):
        return self._players

    @property
    def admin(self) -> Player:
        return self._admin

    def add_player(self, player_name: str):
        player = Player(player_name)
        if self.players == []:
            self._admin = player
        self.players.append(Player(player_name))

    def get_lobby_json(self) -> str:
        return json.dumps(
            {
                "player_list": [player.name for player in self.players],
                "running": self._running,
                "admin": self.admin.name,
            }
        )

    def _get_n_evil_team(self) -> int:
        match len(self.players):
            case 4:
                return 1
            case 5 | 6:
                return 2
            case 7 | 8:
                return 3
            case _:
                raise Exception("Wrong number of players")

    def start_game(self):
        if not 4 <= len(self.players) <= 8:
            print(
                f"Error: Game only support 4-8 players, current players {len(self.players)}"
            )
            return
        if self._state == GameState.STARTED:
            print("Error: The game has already started")
            return

        # assign team
        random.shuffle(self._players)
        n_evil = self._get_n_evil_team()
        n_good = len(self.players) - n_evil
        for n, team in enumerate([Team.EVIL] * n_evil + [Team.GOOD] * n_good):
            self.players[n].set_team(team)

        # assign captain
        self.players[0].set_role(Role.CAPTAIN)

        # assign roles
        roles = [Role(n) for n in range(1, 13)]
        random.shuffle(roles)
        [p.set_role(r) for p, r in zip(self.players, roles)]

        # assign infected player
        random.choice(self.players).set_infected(True)

        assert all([p.team is not None for p in self.players])
        assert len(set([p.role for p in self.players])) == len(self.players)
        assert len(set([p.role for p in self.players])) == len(self.players)

        self._state = GameState.STARTED
        return

    def get_players_json(self) -> str:
        if self._state != GameState.STARTED:
            return "{players: []}"

        return json.dumps(
            {
                "assigned_characters": dict(
                    [(p.name, {"character": p.role.value}) for p in self.players]
                )
            }
        )


if __name__ == "__main__":
    game = GameRoom()
    game.add_player("1")
    game.add_player("2")
    game.add_player("3")
    game.add_player("4")
    game.start_game()
    print(game.get_players_json())
