import cv2
import numpy as np
from PySide6.QtCore import QThread, Signal

from utils.hand_gesture_image_collector import HandGestureImageCollector


class VideoThread(QThread):
    change_pixmap_signal = Signal(np.ndarray, object, object)
    image_collector = HandGestureImageCollector(256)

    def run(self):
        while True:
            img, img_white, normalized_position = self.image_collector.get_image(256)
            self.change_pixmap_signal.emit(img, img_white, normalized_position)