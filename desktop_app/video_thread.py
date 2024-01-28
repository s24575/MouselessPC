import cv2
import numpy as np
from PySide6.QtCore import QThread, Signal
import time

from utils.hand_gesture_image_collector import HandGestureImageCollector


class VideoThread(QThread):
    change_pixmap_signal = Signal(np.ndarray)
    image_collector = HandGestureImageCollector()
    gesture_signal = Signal(str)
    process_gestures = False

    def __init__(self, gesture_manager):
        self.gesture_manager = gesture_manager
        super().__init__()

    def run(self):
        while True:
            success, image = self.image_collector.get_current_image()
            if not success:
                time.sleep(1)
                continue

            image = cv2.flip(image, 1)
            self.change_pixmap_signal.emit(image)

            if self.process_gestures:
                hand_landmarks, main_landmark_position = self.image_collector.get_landmark_positions(image)
                if hand_landmarks is not None:
                    gesture = self.gesture_manager.activate(hand_landmarks, main_landmark_position)
                    self.gesture_signal.emit(gesture)

    def change_video_source(self, url):
        self.image_collector.camera = url
