from dataclasses import dataclass
import math
from typing import Any, Optional, Tuple

import cv2
import numpy as np
from utils.camera import Camera
from cvzone.HandTrackingModule import HandDetector

from utils.enums import KeyAction


@dataclass
class NormalizedPosition:
    """
    Mouse/hand position on the screen/image normalized to range [0.0, 1.0]
    """
    x: float
    y: float


class HandGestureImageCollector:
    def __init__(self, img_size: int):
        self._img_size = img_size
        self._camera = Camera()
        self._detector = HandDetector(maxHands=1)

    def __del__(self):
        cv2.destroyAllWindows()
     
    def collect_image(self):
        print(f"Press {KeyAction.SAVE.value} to save the current image")
        while True:
            collect: bool = False
            key = cv2.waitKey(1)
            if key == ord(KeyAction.QUIT.value):
                return None
            elif key == ord(KeyAction.SAVE.value):
                collect = True
            
            img, hand_img, _ = self.get_image(self._img_size)
            if img is not None:
                cv2.imshow("Image", img)
            if hand_img is not None:
                cv2.imshow("Image modified", hand_img)
                if collect:
                    return hand_img

    def get_image(self, img_size: int, flip_img: bool = True) -> Optional[Tuple[Any, Any, NormalizedPosition]]:
        img, img_white, normalized_position = None, None, None
        success, img = self._camera.get_current_image()
        if success:
            if flip_img:
                img = cv2.flip(img, 1)
            hands, img = self._detector.findHands(img)
            if hands:
                img_white, normalized_position = self.get_hand_image(hands[0], img, img_size, 15)

        return img, img_white, normalized_position
    
    @staticmethod
    def get_hand_image(hand, img, img_size: int, padding: int = 0):
        img_height, img_width, _ = img.shape
        x, y, w, h = hand['bbox']
        x1, x2, y1, y2 = HandGestureImageCollector.get_hand_bbox_vertex_positions(x, y, w, h, img_width, img_height,
                                                                                  padding)
        crop_width, crop_height = x2 - x1, y2 - y1

        if crop_width > 0 and crop_height > 0:
            x_norm = (x1 + crop_width / 2) / img_width
            y_norm = (y1 + crop_height / 2) / img_height
            normalized_position = NormalizedPosition(x_norm, y_norm)
            img_crop = img[y1:y2, x1:x2]

            max_length = max(crop_width, crop_height)
            scale_ratio = img_size / max_length

            crop_width = int(crop_width * scale_ratio)
            crop_height = int(crop_height * scale_ratio)

            img_resized = cv2.resize(img_crop, (crop_width, crop_height))

            gap_h = math.ceil((img_size - crop_height) / 2)
            gap_w = math.ceil((img_size - crop_width) / 2)

            img_white = np.ones((img_size, img_size, 3), np.uint8) * 255
            img_white[gap_h:gap_h + crop_height, gap_w:gap_w + crop_width] = img_resized

            return img_white, normalized_position

        return None, None

    @staticmethod
    def get_hand_bbox_vertex_positions(hand_x: int, hand_y: int, hand_width: int, hand_height: int,
                                       img_width: int, img_height: int, padding: int = 0) -> Tuple[int, int, int, int]:
        x1 = max(hand_x - padding, 0)
        y1 = max(hand_y - padding, 0)
        x2 = min(hand_x + hand_width + padding, img_width)
        y2 = min(hand_y + hand_height + padding, img_height)
        return x1, x2, y1, y2
