from typing import Tuple

import pyautogui

from utils.consts import Consts
from utils.enums import MouseAction


class MouseController:
    @staticmethod
    def get_screen_size() -> Tuple[int, int]:
        size = pyautogui.size()
        return size.width, size.height

    @staticmethod
    def get_mouse_position() -> Tuple[int, int]:
        position = pyautogui.position()
        return int(position.x), int(position.y)

    @staticmethod
    def left_click():
        pyautogui.click()

    @staticmethod
    def double_left_click():
        pyautogui.doubleClick()

    @staticmethod
    def right_click():
        pyautogui.rightClick()

    @staticmethod
    def middle_click():
        pyautogui.middleClick()

    @staticmethod
    def move_to(x: int, y: int, duration: int = 0.1):
        pyautogui.moveTo(x, y, duration=duration)

    @staticmethod
    def drag_to(x: int, y: int, duration: int = 0.1):
        pyautogui.dragTo(x, y, duration=duration)

    @staticmethod
    def move_relative(x: int, y: int, duration: int = 0.1):
        pyautogui.moveRel(x, y, duration=duration)

    @staticmethod
    def calculate_mouse_position(normalized_x: int, normalized_y: int,
                                 screen_width: int, screen_height: int,
                                 margin: int = Consts.SCREEN_MARGIN) -> Tuple[int, int]:
        # Calculate position in the inner rectangle's coordinate system
        x = normalized_x * (screen_width + 2 * margin) - margin
        y = normalized_y * (screen_height + 2 * margin) - margin

        return x, y

    @staticmethod
    def execute_mouse_action(mouse_action: MouseAction):
        match mouse_action:
            case MouseAction.LEFT_CLICK:
                MouseController.left_click()
            case MouseAction.DOUBLE_LEFT_CLICK:
                MouseController.double_left_click()
            case MouseAction.RIGHT_CLICK:
                MouseController.right_click()
            case MouseAction.MIDDLE_CLICK:
                MouseController.middle_click()
