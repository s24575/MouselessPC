from enum import Enum


class MouseAction(Enum):
    LEFT_CLICK = 1
    DOUBLE_LEFT_CLICK = 2
    RIGHT_CLICK = 3
    MIDDLE_CLICK = 4


class KeyAction(Enum):
    SAVE = "s"
    QUIT = "q"
