import os
import time
from typing import List

import cv2

from utils.hand_gesture_image_collector import HandGestureImageCollector


class HandGesture:
    def __init__(self, name: str):
        self.name = name

class GestureManager:
    data_dir = "model/data/images"

    def __init__(self):
        self.hand_gestures: List[HandGesture] = []

    def collect_gesture_images(self, samples: int, img_size: int) -> bool:
        hand_gesture_image_collector = HandGestureImageCollector()
        for hand_gesture in self.hand_gestures:
            print(f"Collecting gesture: {hand_gesture.name}")
            for i in range(samples):
                print(f"Collecting image #{i + 1}")
                print(f"Press {HandGestureImageCollector.KeyAction.SAVE.value} to save the displayed image")
                while True:
                    save_image = False
                    if cv2.waitKey(1) == ord(HandGestureImageCollector.KeyAction.QUIT.value):
                        return False
                    elif cv2.waitKey(1) == ord(HandGestureImageCollector.KeyAction.SAVE.value):
                        save_image = True
                    
                    img, hand_img, _ = hand_gesture_image_collector.get_image(img_size)
                    if img is not None:
                        cv2.imshow("Image", img)
                    if save_image and hand_img is not None:
                        self.save_gesture_image(hand_gesture, hand_img)
                        break
        return True

    def save_gesture_image(self, hand_gesture: str, image):
        image_dir = os.path.join(self.data_dir, hand_gesture.name)
        if not os.path.exists(image_dir):
            os.makedirs(image_dir)
        image_filename = f"image_{time.time()}.jpg"
        image_filepath = os.path.join(image_dir, image_filename)
        cv2.imwrite(image_filepath, image)
        print("Image saved successfully.")

    def add_gesture(self, name: str):
        gesture = HandGesture(name)
        self.hand_gestures.append(gesture)
