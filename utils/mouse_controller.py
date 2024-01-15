from typing import Tuple

import pyautogui

from utils.enums import MouseAction


class MouseController:
    @staticmethod
    def get_screen_width_and_height() -> Tuple[int, int]:
        size = pyautogui.size()
        return size.width, size.height

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
    def move_to(x: int, y: int, duration: int = 0):
        pyautogui.moveTo(x, y, duration=duration)

    @staticmethod
    def drag_to(x: int, y: int, duration: int = 0):
        pyautogui.dragTo(x, y, duration=duration)

    @staticmethod
    def move_by(x: int, y: int, duration: int = 0):
        pyautogui.moveRel(x, y, duration=duration)

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
