import sys

import pyautogui
from PySide6.QtWidgets import QApplication

from desktop_app.ui_main_window import UiMainFrame
from utils.enums import MouseAction
from utils.gesture_manager import GestureManager


def main():
    pyautogui.FAILSAFE = False

    samples = 10
    retrain_model = False

    gesture_manager = GestureManager()
    gesture_manager.add_gesture("fist", MouseAction.LEFT_CLICK)
    gesture_manager.add_gesture("palm", MouseAction.NONE)
    gesture_manager.add_gesture("moon", MouseAction.RIGHT_CLICK)

    if retrain_model:
        gesture_manager.train_model(samples)

    gesture_manager.model.init()

    app = QApplication(sys.argv)
    widget = UiMainFrame(gesture_manager)
    widget.show()
    sys.exit(app.exec())


if __name__ == '__main__':
    main()
