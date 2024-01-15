import sys

from PySide6.QtWidgets import QApplication

from desktop_app.ui_main_window import UiMainFrame
from model.model import Model
from utils.enums import MouseAction
from utils.gesture_manager import GestureManager


def main():
    samples = 10
    img_size = 256
    collect_images = False

    gesture_manager = GestureManager()
    gesture_manager.add_gesture("a", MouseAction.LEFT_CLICK)
    gesture_manager.add_gesture("b", MouseAction.RIGHT_CLICK)
    gesture_manager.add_gesture("c", MouseAction.DOUBLE_LEFT_CLICK)

    model = Model(gesture_manager.hand_gestures, img_size)

    if collect_images:
        status = gesture_manager.collect_gesture_images(samples, img_size)

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
