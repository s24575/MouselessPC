import cv2
import numpy as np
from PySide6.QtCore import QThread, Signal


class VideoThread(QThread):
    change_pixmap_signal = Signal(np.ndarray)

    def run(self):
        cap = cv2.VideoCapture(0)
        while True:
            ret, cv_imag = cap.read()
            if ret:
                self.change_pixmap_signal.emit(cv_imag)