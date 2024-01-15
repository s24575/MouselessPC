import time
from PySide6.QtCore import QThread, Signal

from model.model import Model
from utils.mouse_controller import MouseController


class LogThread(QThread):
    def __init__(self, model: Model):
        super().__init__()
        self.img_white = None
        self.normalized_position = None
        self.last_gesture_name = None
        self.model = model
        self.screen_width, self.screen_height = MouseController.get_screen_width_and_height()

    gesture_signal = Signal(str)
    is_stop_time = False

    def run(self):
        while not self.is_stop_time:
            if self.img_white is not None and self.normalized_position is not None:
                gesture = self.activate(self.img_white, self.normalized_position)
                self.img_white = None
                self.normalized_position = None
                self.gesture_signal.emit(gesture)
            time.sleep(0.01)

    def activate(self, img_white, normalized_position):
        hand_gesture, chance = self.model.predict(img_white)

        mouse_x, mouse_y = normalized_position.x * self.screen_width, normalized_position.y * self.screen_height
        MouseController.drag_to(mouse_x, mouse_y)

        if self.last_gesture_name != hand_gesture.name:
            MouseController.execute_mouse_action(hand_gesture.action)

        self.last_gesture_name = hand_gesture.name
        return hand_gesture.name

    def update_image(self, img_white, normalized_position):
        self.img_white = img_white
        self.normalized_position = normalized_position
