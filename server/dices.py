from enum import Enum
import random
import json
import os

class Face(Enum):
    DAMAGE = 1
    PARSITE_SCAN_LR = 2
    ENGINE_POWER_UP = 3
    STALL_ENGINE = 4
    RESHUFFLE = 5
    ID_CHECK = 6
    INSTA_KILL = 7
    QUARANTINE = 8
    CANCEL = 9
    PARSITE_SCAN_ANY = 10


class Dice:
    def __init__(self, faces: tuple[Face, Face, Face, Face, Face, Face]):
        self.faces = faces
        self.current_face = faces[0]
        self.can_be_rerolled = True
        self.rolled_by = None
    @property
    def face(self) -> Face:
        return self.current_face

    def roll(self) -> Face:
        self.current_face = random.choice(self.faces)
        return self.current_face

    def reroll(self) -> Face:
        self.can_be_rerolled = False
        return self.roll()

    def reset(self):
        self.can_be_rerolled = True
        self.rolled_by = None

    def get_state(self) -> dict:
        return {
            "face": self.face.name,
            "face_value": self.face.value,
            "can_be_rerolled": self.can_be_rerolled,
            "all_faces": [f.name for f in self.faces],
            "all_faces_value": [f.value for f in self.faces],
            "rolled_by": self.rolled_by,
        }


class DiceBag:
    def __init__(self):
        dice_data_path = os.path.join(os.path.dirname(__file__), "diceData.json")
        with open(dice_data_path, "r", encoding="utf-8-sig") as f:
           dice_data = json.load(f)
        self.bag: list[Dice] = self._create_dice_from_config(dice_data)

    def _create_dice_from_config(self, dice_data) -> list[Dice]:
       dice_list = []
       for dice_config in dice_data["dice"]:
           faces = tuple(Face(side) for side in dice_config["sides"])
           dice_list.append(Dice(faces))
       return dice_list
            


    def pick_dice(self) -> Dice:
        random.shuffle(self.bag)
        return self.bag.pop()

    def return_dice(self, dice: Dice):
        dice.reset()
        self.bag.append(dice)