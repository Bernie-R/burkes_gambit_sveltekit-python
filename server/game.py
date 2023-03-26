from asyncio import wait
from enum import Enum, IntEnum
from datetime import datetime
from typing import Optional, Self
from dataclasses import dataclass
from dices import DiceBag, Dice, Face
from uuid import uuid4
import random
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


class Action(Enum):
    PICK_AND_ROLL = 1
    REROLL = 2
    USE_RESERVE_DICE = 3
    RESERVE_DICE = 4


@dataclass
class Player:
    def __init__(self, name: str, is_admin=False):
        self.name = name
        self.id = str(uuid4())
        self.helth = 2
        self.is_admin = is_admin
        self.role: Optional[Role] = None
        self.team: Optional[Team] = None
        self.dice: Optional[Dice] = None
        self.last_action: datetime = datetime.now()
        self.is_infected = False

    @property
    def has_dice(self) -> bool:
        return self.dice is not None

    def set_team(self, team: Team) -> Self:
        self.team = team
        return self

    def set_role(self, role: Role) -> Self:
        self.role = role
        return self

    def set_infected(self, is_infected) -> Self:
        self.is_infected = is_infected
        return self

    def reserve_dice(self, dice: Dice):
        self.dice = dice

    def return_dice(self) -> Optional[Dice]:
        if not self.has_dice:
            print("Error: player has no dice")
            return None

        dice = self.dice
        self.dice = None
        return dice

    def __eq__(self, other):
        return self.id == other.id

    def __str__(self):
        return f"Name: {self.name}, id: {self.id}, health: {self.helth}, role: {self.role.name if self.role is not None else ''}, admin: {self.is_admin}"

    def get_state(self, only_public: bool = False) -> dict:
        state = {
            "name": self.name,
            "is_admin": self.is_admin,
            "role": self.role.name if self.role is not None else False,
            "dice": self.dice.get_state() if self.dice is not None else False,
            "last_action": self.last_action.timestamp(),
        }
        if not only_public and self.team is not None:
            state["team"] = (self.team.name,)
            state["id"] = (self.id,)

        return state


class GameRoom:
    def __init__(self, id: str):
        self._id = id
        self._running = True
        self._max_lightning = 3
        self._players: list[Player] = []
        self._admin: Player
        self._state = GameState.LOBBY
        self._dice_bag = DiceBag()
        self._turn = 0
        self.n_power_ups = 0
        self.current_dice: Optional[Dice] = None

    @property
    def id(self):
        return str(self._id)

    @property
    def players(self):
        return self._players

    @property
    def current_player(self) -> Player:
        return self.players[self._turn % len(self.players)]

    @property
    def admin(self) -> Player:
        return self._admin

    def next_turn(self):
        self._turn += 1

    def add_player(self, player_name: str) -> Player:
        player = Player(player_name)
        if self.players == []:
            self._admin = player
        self.players.append(Player(player_name))
        return player

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
        [p.set_role(r) for p, r in zip(self.players[1:], roles)]

        # assign infected player
        random.choice(self.players).set_infected(True)

        assert all(p.team is not None for p in self.players)
        assert all(p.role is not None for p in self.players)
        assert self.current_player.role == Role.CAPTAIN

        self._state = GameState.STARTED
        return

    def execute_action(self, player: Player, action: Action):
        if player != self.current_player:
            print(f"Error: not {player.name}'s turn")
            return
        if self._state != GameState.STARTED:
            print("Error: game is not yet started")
            return

        self._run_action(player, action)

        return self.get_game_state(player)

    def _run_action(self, player: Player, action: Action):
        match action:
            case Action.PICK_AND_ROLL:
                self.current_dice = self._dice_bag.pick_dice()
                if self.current_dice.roll() == Face.ENGINE_POWER_UP:
                    self.n_power_ups += 1
                    self.next_turn()
                return

            case Action.REROLL:
                if self.current_dice is None:
                    print("Error: no dice to reroll")
                    return

                if not self.current_dice.can_be_rerolled:
                    print("Error: dice has already been rerolled")
                    return

                self.current_dice.reroll()

            case Action.USE_RESERVE_DICE:
                if player.dice is None:
                    print("Error: player has no reserved_dice")
                    return

                self.use_dice_action(player, player.dice.face)

            case Action.RESERVE_DICE:
                if self.current_dice is None:
                    print("Error: no current dice to reserve")
                    return

                player.reserve_dice(self.current_dice)
                raise NotImplemented

    def use_dice_action(self, player: Player, face: Face):
        pass

    # TODO: replace this and get_lobby_json with get_game_state(self, player : Player) -> str
    # that returns the whole game state from one players view.
    # The client can then use the state to render everything
    def get_game_state(self, player: Player) -> dict:
        return {
            "state": self._state.name,
            "n_power_ups": self.n_power_ups,
            "self": player.get_state(),
            "current_player": self.current_player.name,
            # "current_dice": self.current_dice.get_state() if self.current_dice is not None else None,
            # "players": [p.get_state(only_public = True) for p in self.players],
        }

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

    def get_lobby_json(self) -> str:
        return json.dumps(
            {
                "player_list": [player.name for player in self.players],
                "running": self._running,
                "admin": self.admin.name,
            }
        )


if __name__ == "__main__":
    game = GameRoom("1")
    p1 = game.add_player("1")
    p2 = game.add_player("2")
    p3 = game.add_player("3")
    p4 = game.add_player("4")
    game.start_game()
    print(json.dumps(p1.get_state()))
    assert game._admin == p1
    game.execute_action(p1, Action.PICK_AND_ROLL)
    print(game.get_players_json())
    print(json.dumps(game.get_game_state(p1)))
