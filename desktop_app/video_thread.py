import cv2
import numpy as np
from PySide6.QtCore import QThread, Signal
import time

from model.model import Model
from utils.hand_gesture_image_collector import HandGestureImageCollector
from utils.mouse_controller import MouseController


class VideoThread(QThread):
    change_pixmap_signal = Signal(np.ndarray)
    image_collector = HandGestureImageCollector()
    gesture_signal = Signal(str)
    process_gestures = False

    def __init__(self, model: Model):
        super().__init__()

        self.screen_width, self.screen_height = MouseController.get_screen_width_and_height()
        self.model = model
        self.previous_gesture_name = None

    def run(self):
        while True:
            success, image = self.image_collector.get_current_image()
            if not success:
                time.sleep(1)
                continue
            image = cv2.flip(image, 1)
            self.change_pixmap_signal.emit(image)
            hand_landmarks, main_landmark_position = self.image_collector.get_landmark_positions(image)
            if self.process_gestures and hand_landmarks is not None:
                gesture = self.activate(hand_landmarks, main_landmark_position)
                self.gesture_signal.emit(gesture)

    def activate(self, hand_landmarks, main_landmark_position):
        hand_gesture, chance = self.model.predict(hand_landmarks)
        print(hand_gesture, chance)
        x_norm, y_norm = main_landmark_position.x, main_landmark_position.y
        x, y = x_norm * self.screen_width, y_norm * self.screen_height
        MouseController.move_to(x, y)

        if self.previous_gesture_name != hand_gesture.name and chance > 0.80:
            MouseController.execute_mouse_action(hand_gesture.action)

            self.previous_gesture_name = hand_gesture.name

        return hand_gesture.name

    def change_video_source(self, url):
        self.image_collector.camera = url
