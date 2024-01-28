from enum import Enum


class Gesture(Enum):
    FIST = 0
    PALM = 1
    MOON = 2
    POINTING_UP = 3
    POINTING_DOWN = 4


class Action(Enum):
    DEFAULT = 1
    LEFT_CLICK = 2
    DOUBLE_LEFT_CLICK = 3
    RIGHT_CLICK = 4
    MIDDLE_CLICK = 5

    VOLUME_UP = 64
    VOLUME_DOWN = 65

    SWITCH_TO_SOUND_MODE = 128


class GestureMode:
    DEFAULT = 1
    SOUND = 2


class KeyAction(Enum):
    SAVE = "s"
    QUIT = "q"
