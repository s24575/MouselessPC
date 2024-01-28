from dataclasses import dataclass

from utils.enums import Action


@dataclass
class HandGestureAction:
    name: str
    action: Action
