from enum import Enum


class MouseAction(Enum):
    NONE = 1
    LEFT_CLICK = 2
    DOUBLE_LEFT_CLICK = 3
    RIGHT_CLICK = 4
    MIDDLE_CLICK = 5


class KeyAction(Enum):
    SAVE = "s"
    QUIT = "q"
