# file: server\game.py
from asyncio import wait
from enum import Enum, IntEnum
from datetime import datetime
from typing import Optional, Self
from dataclasses import dataclass
from dices import DiceBag, Dice, Face
from uuid import uuid4

import random
import json
import os

class GameState(IntEnum):
    LOBBY = 1
    STARTED = 2
    END_GAME = 3

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
    ENGINEER = 10

class Action(Enum):
    PICK_AND_ROLL = 1
    REROLL = 2
    USE_RESERVE_DICE = 3
    RESERVE_DICE = 4
    CHARACTER_POWER = 5
    END_TURN = 6
    USE_DICE_ACTION = 7

class HistoryEvent:
    def __init__(self, player: str, action: Action, dice_face: Optional[Face] = None, target_player: Optional[str] = None):
        self.player = player
        self.action = action
        self.dice_face = dice_face.name if dice_face else None
        self.target_player = target_player

    def to_dict(self) -> dict:
        return {
            "player": self.player,
            "action": self.action.name,
            "dice_face": self.dice_face,
            "target_player": self.target_player,
        }

class History:
    def __init__(self):
        self.events: list[HistoryEvent] = []

    def add_event(self, event: HistoryEvent):
        self.events.append(event)

    def get_public_events(self) -> list[dict]:
        return [event.to_dict() for event in self.events]

# Load character descriptions once
characters_path = os.path.join(os.path.dirname(__file__), "characters.json")
with open(characters_path, "r") as f:
    CHARACTERS = json.load(f)

@dataclass
class Player:
    def __init__(self, name: str, is_admin=False, websocket=None):
        self.name = name
        self.id = str(uuid4())
        self.health = 2
        self.is_admin = is_admin
        self.role: Optional[Role] = None
        self.team: Optional[Team] = None
        self.dice: Optional[Dice] = None
        self.last_action: datetime = datetime.now()
        self.is_infected = False
        self.used_power = False
        self.websocket = websocket
        self.is_dead = False
        self.is_quarantined = False
        self.scan_result: Optional[str] = None
        self.id_check_result: Optional[str] = None

    @property
    def has_dice(self) -> bool:
        return self.dice is not None
    
    @property
    def get_scan_result(self):
        return self.scan_result
    
    @property
    def get_id_check_result(self):
        return self.id_check_result

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
    
    def set_quarantined(self, is_quarantined: bool) -> Self:
        self.is_quarantined = is_quarantined
        return self
    
    def set_scan_result(self, result: str):
         self.scan_result = result
    
    def set_id_check_result(self, result: str):
         self.id_check_result = result
    
    def set_dead(self) -> Self:
        self.is_dead = True
        return self

    def __eq__(self, other):
        return self.id == other.id

    def __str__(self):
        return f"Name: {self.name}, id: {self.id}, health: {self.health}, role: {self.role.name if self.role is not None else ''}, admin: {self.is_admin}"

    def get_state(self, only_public: bool = False) -> dict:
         state = {
            "name": self.name,
            "is_admin": self.is_admin,
            "role": self.role.name if self.role is not None else False,
            "dice": self.dice.get_state() if self.dice is not None else False,
            "health": self.health,
            "last_action": self.last_action.timestamp(),
            "role_description": CHARACTERS.get(self.role.name, "") if self.role else "",
            "used_power": self.used_power,  # add this to track used power
            "is_dead": self.is_dead,
            "is_quarantined": self.is_quarantined,

        }
         if not only_public and self.team is not None:
             state["id"] = (self.id,)
             state["team"] = self.team.name if self.team else False,
             state["scan_result"] = self.scan_result,
             state["id_check_result"] = self.id_check_result

         return state

class GameRoom:
    def __init__(self, id: str):
        self._id = id
        self._running = 1
        self._max_lightning = 3
        self._players: list[Player] = []
        self._admin: Player
        self._state = GameState.LOBBY
        self._dice_bag = DiceBag()
        self._turn = 0
        self.n_power_ups = 0
        self.current_dice: Optional[Dice] = None
        self.latest_action: Optional[tuple[str, str]] = None
        self.stall_engine_active = False
        self.quarantined_player: Optional[Player] = None
        self.end_game_votes: dict[str,str] = {}
        self.parasite_cards_order: list[Player] = []
        self.last_scan: Optional[tuple[str, str]] = None
        self.last_id_check: Optional[tuple[str, str]] = None
        self.history = History()

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
    def is_end_game(self) -> bool:
        return self._state == GameState.END_GAME

    @property
    def admin(self) -> Player:
        return self._admin

    def next_turn(self):
         if self.quarantined_player:
           self.quarantined_player.set_quarantined(False)
           self.quarantined_player= None
         self._turn += 1
         self.current_dice = None
         print(self.current_player.name)
         print(self.current_player.health)
         print(self.current_player.is_dead)
         if self.current_player.is_dead:
              self.next_turn()

    def add_player(self, player_name: str, websocket=None) -> Player:
        player = Player(player_name, websocket=websocket)
        if self.players == []:
            self._admin = player
        self.players.append(player)
        return player

    def get_player_by_name(self, name: str) -> Optional[Player]:
        for player in self._players:
            if player.name == name:
                return player
        return None

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
    
    def _get_n_power_ups_endgame(self) -> int:
         match len(self.players):
            case 4:
                return 3
            case 5:
                return 4
            case 6 | 7 | 8:
                return 5
            case _:
                raise Exception("Wrong number of players")
    
    def _reshuffle_parasites(self):
        infected = None
        clean = []

        for player in self.players:
            if player.is_infected:
                infected = player
            else:
                 clean.append(player)
        
        random.shuffle(clean)

        if infected is None:
           print("Error: no infected player found")
           return

        new_parasites = [infected] + clean[1:]
        
        for player in self.players:
            if player == infected:
                player.set_infected(True)
            elif player in new_parasites:
                 player.set_infected(False)
            else:
                player.set_infected(False)
        
        self.parasite_cards_order = self.players.copy()
    
    def _set_parasite_order(self):
        self.parasite_cards_order = self.players.copy()

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

        # assign captain to the first player
        self.players[0].set_role(Role.CAPTAIN)

        # Create a list of all other roles (excluding CAPTAIN)
        all_roles = [
            Role.HACKER, 
            Role.MARINE, 
            Role.COMMUNICATIONS_OFFICER, 
            Role.TECHNICIAN, 
            Role.AUGMENTED, 
            Role.SECURITY_OFFICER, 
            Role.DOCTOR, 
            Role.PERSONAL_OFFICER, 
            Role.ENGINEER
        ]

        # Shuffle and assign these roles to the other players
        random.shuffle(all_roles)
        for player, role in zip(self.players[1:], all_roles):
            player.set_role(role)

        # assign infected player
        random.choice(self.players).set_infected(True)
        self._set_parasite_order()
        assert all(p.team is not None for p in self.players)
        assert all(p.role is not None for p in self.players)
        assert self.current_player.role == Role.CAPTAIN

        self._state = GameState.STARTED
        return

    def execute_action(self, player: Player, action: Action):
        if player != self.current_player and action != Action.CHARACTER_POWER:
            print(f"Error: not {player.name}'s turn")
            return
        if self._state != GameState.STARTED and self._state != GameState.END_GAME :
            print(f"Error: game is not yet started")
            return
        
        if player.is_dead:
            print(f"Error: {player.name} is dead")
        
        if player.is_quarantined and action != Action.CHARACTER_POWER:
           print(f"Error: {player.name} is quarantined")
           return
        
        self._run_action(player, action)
        return self.get_game_state(player)

    def _run_action(self, player: Player, action: Action):
        self.latest_action = (player.name, action.name)
        match action:
            case Action.PICK_AND_ROLL:
                self.current_dice = self._dice_bag.pick_dice()
                self.current_dice.rolled_by = player.name # Added this line
                face = self.current_dice.roll()
                self.history.add_event(HistoryEvent(player.name, action, face))
                if face == Face.ENGINE_POWER_UP:
                    if not self.stall_engine_active:
                        self.n_power_ups += 1
                    else:
                        self.stall_engine_active = False
                    self.next_turn()
                    if self.n_power_ups >= self._get_n_power_ups_endgame():
                        self._state = GameState.END_GAME;
                return

            case Action.REROLL:
                if self.current_dice is None:
                    print("Error: no dice to reroll")
                    return

                if not self.current_dice.can_be_rerolled:
                    print("Error: dice has already been rerolled")
                    return

                face = self.current_dice.reroll()
                self.history.add_event(HistoryEvent(player.name, action, face))
                if face == Face.ENGINE_POWER_UP:
                    if not self.stall_engine_active:
                        self.n_power_ups += 1
                    else:
                        self.stall_engine_active = False
                    self.next_turn()
                    if self.n_power_ups >= self._get_n_power_ups_endgame():
                        self._state = GameState.END_GAME;

            case Action.USE_RESERVE_DICE:
                if player.dice is None:
                    print("Error: player has no reserved_dice")
                    return

                self.use_dice_action(player, player.dice.face, player)

            case Action.RESERVE_DICE:
                if self.current_dice is None:
                    print("Error: no current dice to reserve")
                    return
                
                if player.dice is not None:
                  self._dice_bag.return_dice(player.return_dice())

                player.reserve_dice(self.current_dice)
                self.history.add_event(HistoryEvent(player.name, action, self.current_dice.face))
                self.next_turn()

            case Action.END_TURN:
                self.next_turn()
                return
    
    def add_vote(self, player: Player, vote: str):
        if player.is_dead:
            print("Error: Dead players cannot vote")
            return

        if vote not in [p.name for p in self.players]:
           print("Error: Trying to vote to non-existent player")
           return
        
        self.end_game_votes[player.name] = vote

    def resolve_end_game(self):
        if self._state != GameState.END_GAME:
            print("Error: game is not in end game")
            return
        
        if len(self.end_game_votes) != len(self.players):
             print("Error: not everyone has voted")
             return

        
        votes = {}

        for vote_player in self.end_game_votes.values():
           if vote_player not in votes:
              votes[vote_player] = 0;
           votes[vote_player] +=1
        
        max_votes = 0
        most_voted_players = []
        for player, vote_count in votes.items():
            if vote_count > max_votes:
               max_votes = vote_count
               most_voted_players = [player]
            elif vote_count == max_votes:
                 most_voted_players.append(player)
        
        if len(most_voted_players) == 0:
             return None;

        if len(most_voted_players) > 1:
            if not any(p.role == Role.CAPTAIN and not p.is_dead for p in self.players) :
                return None;
            else:
                captain = next(p for p in self.players if p.role == Role.CAPTAIN and not p.is_dead)
                player_to_sacrifice = next(p for p in self.players if p.name == self.end_game_votes[captain.name])
                return player_to_sacrifice;
        else:
            return next(p for p in self.players if p.name == most_voted_players[0] )

    def use_dice_action(self, player: Player, face: Face, target_player = None):
            self.history.add_event(HistoryEvent(player.name, Action.USE_DICE_ACTION, face, target_player.name if target_player else None))
            match face:
                case Face.DAMAGE:
                     if target_player is None:
                       self._apply_damage_or_heal(player, -1)
                     else:
                       self._apply_damage_or_heal(target_player, -1)
                case Face.PARSITE_SCAN_LR:
                    self.scan_parasite(player, target_player)
                case Face.ENGINE_POWER_UP:
                     print("Error: Engine power up can't be activated in this stage")
                     pass

                case Face.STALL_ENGINE:
                    self.stall_engine_active = True
                    #  logic for setting stall engine
                    pass
                case Face.RESHUFFLE:
                     self._reshuffle_parasites()
                 
                case Face.ID_CHECK:
                     self.id_check(player, target_player)
                case Face.INSTA_KILL:
                     if target_player is not None:
                       self._apply_damage_or_heal(target_player, -3) # for now kill self
                case Face.QUARANTINE:
                     if target_player is not None:
                        self.quarantined_player = target_player.set_quarantined(True)
                case Face.CANCEL:
                     print(f"{player.name} cancelled something")
                    # Logic for cancel action
                     pass
                case Face.PARSITE_SCAN_ANY:
                    self.scan_parasite(player, target_player)

    def scan_parasite(self, player: Player, target_player: Player):
            if target_player is None:
                print("Error: No target player to scan")
                return

            self.last_scan = (player.name, target_player.name)  # Log who initiated the scan and who was scanned
            scan_result = f"{'Infected' if target_player.is_infected else 'Clean'}"
        
            player.set_scan_result(scan_result) # Store scan result for the active player
            
            return scan_result  # Return the scan result

    def id_check(self, player: Player, active_player: Optional[Player]):
        if active_player is None:
            print("Error: No player selected to id check")
            return

        self.last_id_check = (player.name, active_player.name)
        player.set_id_check_result(f"{active_player.name}'s team is: {active_player.team.name if active_player.team else 'No team'}")

    def _apply_damage_or_heal(self, player:Player, damage_amount:int):
        player.health += damage_amount
        if player.health <= 0:
            player.health = 0
            player.set_dead()

    def get_game_state(self, player: Player) -> dict:
        return {
            "state": self._state.name,
            "n_power_ups": self.n_power_ups,
            "self": player.get_state(only_public = False),
            "current_player": self.current_player.name,
            "roomId": self.id,
            "current_dice": self.current_dice.get_state() if self.current_dice is not None else None,
            "players": [p.get_state(only_public = True) for p in self.players],
            "latest_action": self.latest_action,
            "end_game_votes": self.end_game_votes,
            "is_end_game": self.is_end_game,
            "last_scan": self.last_scan,
             "scan_result": player.get_scan_result if not player.get_scan_result is None else False,
            "last_id_check": self.last_id_check,
             "id_check_result": player.get_id_check_result if not player.get_id_check_result is None else False,
            "history": self.history.get_public_events(),  
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

    def get_lobby_json(self) -> dict:
        return {
                "player_list": [player.name for player in self.players],
                "running": self._state,
                "admin": self.admin.name,
            }

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
    game.execute_action(p1, Action.USE_RESERVE_DICE)
    game.use_dice_action(p1,Face.PARSITE_SCAN_LR)
    game.use_dice_action(p1,Face.ID_CHECK,p2)
    game._apply_damage_or_heal(p2,-2) # Kill p2
    game.execute_action(p1, Action.END_TURN)

    print(p1.scan_result)
    print(p1.id_check_result)
    print(game.get_players_json())
    print(json.dumps(game.get_game_state(p1)))
    assert game.current_player != p2 # It should go to p3 since p2 is dead