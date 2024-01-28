import cv2


class Camera:
    def __init__(self, url=0):
        self.cap = cv2.VideoCapture(url)

    def __del__(self):
        self.cap.release()

    def get_current_image(self):
        success, img = self.cap.read()
        return success, img
