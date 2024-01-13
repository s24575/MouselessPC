import time

import keyboard
from PySide6.QtCore import QThread, Signal, Slot

from desktop_app.gesture_service import GestureService
from utils.windows_mouse_controller import WindowsMouseController


class LogThread(QThread):
    def __init__(self, model):
        super().__init__()
        self.mouse_controller = WindowsMouseController(model)
        self.img_white = None
        self.normalized_position = None
        self.last_gesture = None

    gesture_signal = Signal(str)
    is_stop_time = False

    def run(self):
        while True:
            if self.is_stop_time:
                break
            if self.img_white is not None and self.normalized_position is not None:
                gesture = self.mouse_controller.activate(self.img_white, self.normalized_position)
                if gesture != self.last_gesture:
                    self.gesture_signal.emit(gesture)
                    self.last_gesture = gesture
            time.sleep(0.1)

    def update_image(self, img_white, normalized_position):
        self.img_white = img_white
        self.normalized_position = normalized_position
