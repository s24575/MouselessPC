import time

import keyboard
from PySide6.QtCore import QThread, Signal

from desktop_app.gesture_service import GestureService


class LogThread(QThread):
    model_controller = GestureService()
    gesture = Signal(str)
    is_stop_time = False

    def run(self):
        while True:
            if self.is_stop_time:
                break
            time.sleep(0.1)
            key = keyboard.read_key()

            # Adjust during integration
            self.model_controller.process_gestures(key)
            self.gesture.emit(key)
