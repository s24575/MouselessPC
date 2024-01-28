import sys

import pyautogui
from PySide6.QtWidgets import QApplication

from desktop_app.ui_main_window import UiMainFrame
from utils.enums import Action, Gesture
from utils.gesture_manager import GestureManager


def main():
    pyautogui.FAILSAFE = False

    samples = 25
    retrain_model = False

    gesture_manager = GestureManager()
    gesture_manager.add_gesture_action(Gesture.FIST, Action.LEFT_CLICK)
    gesture_manager.add_gesture_action(Gesture.PALM, Action.DEFAULT)
    gesture_manager.add_gesture_action(Gesture.MOON, Action.SWITCH_TO_SOUND_MODE)
    gesture_manager.add_gesture_action(Gesture.POINTING_UP, Action.VOLUME_UP)
    gesture_manager.add_gesture_action(Gesture.POINTING_DOWN, Action.VOLUME_DOWN)

    if retrain_model:
        gesture_manager.train_model(samples)

    gesture_manager.model.init()

    app = QApplication(sys.argv)
    widget = UiMainFrame(gesture_manager)
    widget.show()
    sys.exit(app.exec())


if __name__ == '__main__':
    main()
