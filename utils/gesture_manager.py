import os
import time
from dataclasses import dataclass
from typing import List

import cv2

from utils.enums import MouseAction
from utils.hand_gesture_image_collector import HandGestureImageCollector


@dataclass
class HandGesture:
    name: str
    action: MouseAction


class GestureManager:
    data_dir = "model/data/images"

    def __init__(self):
        self.hand_gestures: List[HandGesture] = []

    def collect_gesture_images(self, samples: int, img_size: int) -> bool:
        image_collector = HandGestureImageCollector(img_size)
        for hand_gesture in self.hand_gestures:
            print(f"Collecting gesture: {hand_gesture.name}")
            for i in range(samples):
                print(f"Collecting image #{i + 1}")
                hand_img = image_collector.collect_image()
                if hand_img is None:
                    return False
                
                self.save_gesture_image(hand_gesture.name, hand_img)
        return True

    def save_gesture_image(self, hand_gesture_name: str, image):
        image_dir = os.path.join(self.data_dir, hand_gesture_name)
        if not os.path.exists(image_dir):
            os.makedirs(image_dir)
        image_filename = f"image_{time.time()}.jpg"
        image_filepath = os.path.join(image_dir, image_filename)
        cv2.imwrite(image_filepath, image)
        print("Image saved successfully.")

    def add_gesture(self, name: str, action: MouseAction):
        gesture = HandGesture(name, action)
        self.hand_gestures.append(gesture)
