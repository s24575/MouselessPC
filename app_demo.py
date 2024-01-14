import sys

import tensorflow as tf
from PySide6.QtWidgets import QApplication

from desktop_app.ui_main_window import UiMainFrame
from model.model import Model
from utils.gesture_manager import GestureManager
from utils.windows_mouse_controller import WindowsMouseController


def main():
    SAMPLES = 10
    IMG_SIZE = 256
    COLLECT_IMAGES = False

    gesture_manager = GestureManager()
    gesture_manager.add_gesture("a")
    gesture_manager.add_gesture("b")
    gesture_manager.add_gesture("c")

    model = Model(gesture_manager.hand_gestures, IMG_SIZE)

    if COLLECT_IMAGES:
        status = gesture_manager.collect_gesture_images(SAMPLES, IMG_SIZE)

        if status is False:
            print("Collecting images was cancelled, exiting...")
            return
        
        model.train()
        model.save_to_file()
    else:
        model.load_from_file()
    
    app = QApplication(sys.argv)
    widget = UiMainFrame(model)
    widget.show()
    sys.exit(app.exec())


if __name__ == '__main__':
    main()
