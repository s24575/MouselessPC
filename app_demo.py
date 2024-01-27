import sys

import pyautogui
from PySide6.QtWidgets import QApplication

from desktop_app.ui_main_window import UiMainFrame
from model.model import Model
from utils.enums import MouseAction
from utils.gesture_manager import GestureManager


def main():
    pyautogui.FAILSAFE = False

    samples = 10
    collect_images = False

    gesture_manager = GestureManager()
    gesture_manager.add_gesture("fist", MouseAction.LEFT_CLICK)
    gesture_manager.add_gesture("palm", MouseAction.NONE)
    gesture_manager.add_gesture("moon", MouseAction.RIGHT_CLICK)

    model = Model(gesture_manager.hand_gestures)

    if collect_images:
        status = gesture_manager.collect_gesture_images(samples)

        if status is False:
            print("Collecting images was cancelled, exiting...")
            return
        
        model.train()

    model.init()
    app = QApplication(sys.argv)
    widget = UiMainFrame(model)
    widget.show()
    sys.exit(app.exec())


if __name__ == '__main__':
    main()
