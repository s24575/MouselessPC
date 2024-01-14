from enum import Enum
import cv2
import pyautogui

from utils.hand_gesture_image_collector import HandGestureImageCollector


class WindowsMouseController:
    class Actions(Enum):
        LEFT_CLICK = 1
        RIGHT_CLICK = 2
        MIDDLE_CLICK = 3
        DOUBLE_CLICK = 4

    def __init__(self, model):
        self.model = model
        self.screen_width, self.screen_height = pyautogui.size()
        self.last_gesture = None

    def move_to_coordinates(self, x, y):
        pyautogui.moveTo(x, y)

    def click(self):
        print("click")
        pyautogui.click()

    def double_click(self):
        print("double click")
        pyautogui.doubleClick()

    def right_click(self):
        print("right click")
        pyautogui.rightClick()

    def drag_to(self, x, y, duration: int = 0):
        pyautogui.dragTo(x, y, duration=duration)
    
    def move_by(self, x, y, duration: int = 0):
        print(f"move by {x},{y}")
        pyautogui.moveRel(x, y, duration=duration)
    
    def activate(self, img_white, normalized_position):
        if img_white is None:
            pass

        prediction, chance = self.model.predict(img_white)

        x, y = normalized_position.x * self.screen_width, normalized_position.y * self.screen_height
        self.drag_to(x, y)

        if self.last_gesture != prediction:
            if prediction == 'b':
                self.click()
            elif prediction == 'c':
                self.right_click()

        self.last_gesture = prediction
        return prediction
