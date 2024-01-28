from dataclasses import dataclass

from utils.enums import MouseAction


@dataclass
class HandGesture:
    name: str
    action: MouseAction
