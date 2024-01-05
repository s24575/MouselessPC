import tensorflow as tf
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

    if COLLECT_IMAGES:
        status = gesture_manager.collect_gesture_images(SAMPLES, IMG_SIZE)

        if status is False:
            print("Collecting images was cancelled, exiting...")
            return
    
    model = Model(gesture_manager.hand_gestures, IMG_SIZE)
    
    if COLLECT_IMAGES:
        model.train()
    
    model.load_from_file()
    
    mouse_controller = WindowsMouseController()
    mouse_controller.activate(model, IMG_SIZE)


if __name__ == '__main__':
    main()