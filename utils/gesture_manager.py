import csv
import os
import time
from typing import List

import cv2

from model.model import Model
from utils.consts import Consts
from utils.enums import Action, GestureMode, Gesture
from utils.hand_gesture_image_collector import HandGestureImageCollector
from utils.mouse_controller import MouseController
from utils.utils import HandGestureAction


class GestureManager:
    data_dir = "model/data/images"

    def __init__(self):
        self.hand_gestures: List[HandGestureAction] = []
        self.screen_width, self.screen_height = MouseController.get_screen_size()
        self.model = Model(self.hand_gestures)
        self.previous_gesture_name = None
        self.mode = GestureMode.DEFAULT
        self.initial_sound_mode_position_y = 0

    def activate(self, hand_landmarks, normalized_position):
        hand_gesture, chance = self.model.predict(hand_landmarks)

        minimum_certainty = 0.80
        if chance > minimum_certainty:
            x, y = MouseController.calculate_mouse_position(normalized_position.x, normalized_position.y,
                                                            self.screen_width, self.screen_height)

            self.handle_gesture(hand_gesture, x, y)
            self.previous_gesture_name = hand_gesture.name

        return hand_gesture.name

    def handle_gesture(self, hand_gesture: HandGestureAction, x: int, y: int):
        if self.mode == GestureMode.DEFAULT:
            if hand_gesture.action == Action.SWITCH_TO_SOUND_MODE:
                self.mode = GestureMode.SOUND
            else:
                MouseController.move_to(x, y)
                if self.previous_gesture_name != hand_gesture.name:
                    MouseController.execute_mouse_action(hand_gesture.action)
        elif self.mode == GestureMode.SOUND:
            if hand_gesture.action == Action.DEFAULT:
                self.mode = GestureMode.DEFAULT
            else:
                MouseController.execute_mouse_action(hand_gesture.action)

    def collect_gesture_images(self, samples: int) -> bool:
        image_collector = HandGestureImageCollector()
        for gesture_index, gesture in enumerate(self.hand_gestures):
            print(f"Collecting gesture: {gesture.name}")
            for i in range(samples):
                print(f"Collecting image #{i + 1}")
                landmark_list = image_collector.collect_landmarks()
                if landmark_list is None:
                    return False

                self.save_landmarks(gesture_index, landmark_list)
        return True

    def train_model(self, samples: int):
        status = self.collect_gesture_images(samples)

        if status is False:
            print("Collecting images was cancelled, exiting...")
            return

        self.model.train()

    def save_gesture_image(self, hand_gesture_name: str, image):
        image_dir = os.path.join(self.data_dir, hand_gesture_name)
        if not os.path.exists(image_dir):
            os.makedirs(image_dir)
        image_filename = f"image_{time.time()}.jpg"
        image_filepath = os.path.join(image_dir, image_filename)
        cv2.imwrite(image_filepath, image)
        print("Image saved successfully.")

    @staticmethod
    def save_landmarks(gesture_index, landmark_list):
        with open(Consts.LANDMARKS_PATH, 'a', newline="") as file:
            writer = csv.writer(file)
            writer.writerow([gesture_index, *landmark_list])
        return

    def add_gesture_action(self, gesture: Gesture, action: Action):
        gesture_action = HandGestureAction(str(gesture), action)
        self.hand_gestures.append(gesture_action)
