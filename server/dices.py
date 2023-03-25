from enum import Enum
import random


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

    def get_state(self) -> dict:
        return {
            "face": self.face.name,
            "can_be_rerolled": self.can_be_rerolled,
            "all_faces": self.faces,
        }


class DiceBag:
    def __init__(self):
        # TODO: Init correct dice bag
        self.bag: list[Dice] = [
            Dice(
                (
                    Face.DAMAGE,
                    Face.PARSITE_SCAN_LR,
                    Face.ENGINE_POWER_UP,
                    Face.STALL_ENGINE,
                    Face.RESHUFFLE,
                    Face.ID_CHECK,
                )
            ),
            Dice(
                (
                    Face.DAMAGE,
                    Face.PARSITE_SCAN_LR,
                    Face.ENGINE_POWER_UP,
                    Face.STALL_ENGINE,
                    Face.RESHUFFLE,
                    Face.ID_CHECK,
                )
            ),
            Dice(
                (
                    Face.DAMAGE,
                    Face.PARSITE_SCAN_LR,
                    Face.ENGINE_POWER_UP,
                    Face.STALL_ENGINE,
                    Face.RESHUFFLE,
                    Face.ID_CHECK,
                )
            ),
            Dice(
                (
                    Face.DAMAGE,
                    Face.PARSITE_SCAN_LR,
                    Face.ENGINE_POWER_UP,
                    Face.STALL_ENGINE,
                    Face.RESHUFFLE,
                    Face.ID_CHECK,
                )
            ),
            Dice(
                (
                    Face.DAMAGE,
                    Face.PARSITE_SCAN_LR,
                    Face.ENGINE_POWER_UP,
                    Face.STALL_ENGINE,
                    Face.RESHUFFLE,
                    Face.ID_CHECK,
                )
            ),
            Dice(
                (
                    Face.DAMAGE,
                    Face.PARSITE_SCAN_LR,
                    Face.ENGINE_POWER_UP,
                    Face.STALL_ENGINE,
                    Face.RESHUFFLE,
                    Face.ID_CHECK,
                )
            ),
        ]

    def pick_dice(self) -> Dice:
        random.shuffle(self.bag)
        return self.bag.pop()

    def return_dice(self, dice: Dice):
        dice.reset()
        self.bag.append(dice)
