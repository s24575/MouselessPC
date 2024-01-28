import itertools
import math
import re
from typing import Tuple

import cv2
import numpy as np
import mediapipe as mp
from utils.camera import Camera

from utils.consts import Consts
from utils.enums import KeyAction


class HandGestureImageCollector:
    def __init__(self):
        self._img_size = Consts.HAND_IMG_SIZE
        self._camera = Camera()
        self.mp_hands = mp.solutions.hands
        self._hands = self.mp_hands.Hands(max_num_hands=1)

    def __del__(self):
        cv2.destroyAllWindows()

    @property
    def camera(self):
        return self._camera

    @camera.setter
    def camera(self, url: str | int):
        pattern = re.compile("^http://\d{1,3}\.\d{1,3}\.\d{1,3}\.\d{1,3}:\d{0,5}/?.*")
        if re.fullmatch(pattern, str(url)) is None and url != 0:
            raise ValueError("Incorrect video source")

        self._camera = Camera(url)


    def get_current_image(self):
        success, img = self._camera.get_current_image()
        return success, img

    def collect_landmarks(self):
        print(f"Press {KeyAction.SAVE.value} to save the current image")
        while True:
            save = False
            key = cv2.waitKey(1)
            if key == ord(KeyAction.QUIT.value):
                return None
            elif key == ord(KeyAction.SAVE.value):
                save = True

            success, image = self._camera.get_current_image()
            if not success:
                continue

            image = cv2.flip(image, 1)
            cv2.imshow("Image", image)
            landmark_positions, _ = self.get_landmark_positions(image)
            if landmark_positions and save:
                return landmark_positions

    def get_landmark_positions(self, image):
        image = cv2.cvtColor(image, cv2.COLOR_BGR2RGB)
        results = self._hands.process(image)

        if results.multi_hand_landmarks is not None:
            for hand_landmarks, handedness in zip(results.multi_hand_landmarks, results.multi_handedness):
                main_landmark_position = hand_landmarks.landmark[9]
                landmarks = self.calc_landmarks(image, hand_landmarks)
                pre_processed_landmarks = self.pre_process_landmarks(landmarks)
                return pre_processed_landmarks, main_landmark_position
        return None, None

    @staticmethod
    def calc_landmarks(image, landmarks):
        image_width, image_height = image.shape[1], image.shape[0]

        landmark_point = []

        # Keypoint
        for _, landmark in enumerate(landmarks.landmark):
            landmark_x = min(int(landmark.x * image_width), image_width - 1)
            landmark_y = min(int(landmark.y * image_height), image_height - 1)
            # landmark_z = landmark.z

            landmark_point.append([landmark_x, landmark_y])

        return landmark_point

    @staticmethod
    def pre_process_landmarks(landmark_list):

        # Convert to relative coordinates
        base_x, base_y = 0, 0
        for index, landmark_point in enumerate(landmark_list):
            if index == 0:
                base_x, base_y = landmark_point[0], landmark_point[1]

            landmark_list[index][0] = landmark_list[index][0] - base_x
            landmark_list[index][1] = landmark_list[index][1] - base_y

        # Convert to a one-dimensional list
        landmark_list = list(itertools.chain.from_iterable(landmark_list))

        # Normalization
        max_value = max(list(map(abs, landmark_list)))

        def normalize_(n):
            return n / max_value

        landmark_list = list(map(normalize_, landmark_list))

        return landmark_list
    
    @staticmethod
    def get_hand_image(hand, img, img_size: int, padding: int = 0):
        img_height, img_width, _ = img.shape
        x, y, w, h = hand['bbox']
        x1, x2, y1, y2 = HandGestureImageCollector.get_hand_bbox_vertex_positions(x, y, w, h, img_width, img_height,
                                                                                  padding)
        crop_width, crop_height = x2 - x1, y2 - y1

        if crop_width > 0 and crop_height > 0:
            img_crop = img[y1:y2, x1:x2]

            max_length = max(crop_width, crop_height)
            scale_ratio = img_size / max_length

            crop_width = int(crop_width * scale_ratio)
            crop_height = int(crop_height * scale_ratio)

            img_resized = cv2.resize(img_crop, (crop_width, crop_height))

            gap_h = math.ceil((img_size - crop_height) / 2)
            gap_w = math.ceil((img_size - crop_width) / 2)

            hand_img = np.ones((img_size, img_size, 3), np.uint8) * 255
            hand_img[gap_h:gap_h + crop_height, gap_w:gap_w + crop_width] = img_resized

            return hand_img

        return None

    @staticmethod
    def get_hand_bbox_vertex_positions(hand_x: int, hand_y: int, hand_width: int, hand_height: int,
                                       img_width: int, img_height: int, padding: int = 0) -> Tuple[int, int, int, int]:
        x1 = max(hand_x - padding, 0)
        y1 = max(hand_y - padding, 0)
        x2 = min(hand_x + hand_width + padding, img_width)
        y2 = min(hand_y + hand_height + padding, img_height)
        return x1, x2, y1, y2
