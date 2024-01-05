from dataclasses import dataclass
from enum import Enum
import math
from typing import Any, Optional, Tuple

import cv2
import numpy as np
from utils.camera import Camera
from cvzone.HandTrackingModule import HandDetector


@dataclass
class NormalizedPosition:
    """
    Mouse/hand position on the screen/image normalized to range [0.0, 1.0]
    """
    x: float
    y: float


class HandGestureImageCollector:
    class KeyAction(Enum):
        SAVE = "s"
        QUIT = "q"

    def __init__(self):
        self.camera = Camera()
        self.detector = HandDetector(maxHands=1)

    def __del__(self):
        cv2.destroyAllWindows()
    
    def get_image(self, img_size: int, flip_img=True) -> Optional[Tuple[Any, Any]]:
        img, img_white, normalized_position = None, None, None
        success, img = self.camera.get_current_image()
        if success:
            if flip_img:
                img = cv2.flip(img, 1)
            hands, img = self.detector.findHands(img)
            if hands:
                img_white, normalized_position = self.get_hand_image(hands, img, img_size)

        return img, img_white, normalized_position

    @staticmethod
    def get_hand_bbox_coordinates(hand_x: int, hand_y: int, hand_width: int, hand_height: int, img_width: int, img_height: int, padding: int = 0):
        x1 = max(hand_x - padding, 0)
        x2 = min(hand_x + hand_width + padding, img_width)
        y1 = max(hand_y - padding, 0)
        y2 = min(hand_y + hand_height + padding, img_height)
        return x1, x2, y1, y2
    
    @staticmethod
    def get_hand_image(hands, img, img_size: int):
        padding = 15
        img_height, img_width, _ = img.shape
        hand = hands[0]
        x, y, w, h = hand['bbox']
        x1, x2, y1, y2 = HandGestureImageCollector.get_hand_bbox_coordinates(x, y, w, h, img_height, img_width, padding)
        crop_width, crop_height = x2 - x1, y2 - y1

        if crop_width > 0 and crop_height > 0:
            normalized_position = NormalizedPosition((x1 + crop_width / 2) / img_width, (y1 + crop_height / 2) / img_height)
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