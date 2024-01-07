from enum import Enum
import cv2
import pyautogui

from utils.hand_gesture_image_collector import HandGestureImageCollector

class WindowsMouseController:
    class Actions(Enum):
        LEFT_CLICK = 1
        RIGHT_CLICK = 2
        MIDDLE_CLICK = 3
        DOUBLE_CLICK = 4

    def __init__(self):
        pass

    def move_to_coordinates(self, x, y):
        pyautogui.moveTo(x, y)

    def click(self):
        print("click")
        pyautogui.click()

    def double_click(self):
        print("double click")
        pyautogui.doubleClick()

    def right_click(self):
        print("right click")
        pyautogui.rightClick()

    def drag_to(self, x, y, duration: int = 0):
        pyautogui.dragTo(x, y, duration=duration)
    
    def move_by(self, x, y, duration: int = 0):
        print(f"move by {x},{y}")
        pyautogui.moveRel(x, y, duration=duration)
    
    def activate(self, model, img_size: int):
        image_collector = HandGestureImageCollector(img_size)
        screen_width, screen_height = pyautogui.size()
        last_gesture = None
        while True:
            key = cv2.waitKey(1)
            if key == ord("q"):
                break
            img, img_white, normalized_position = image_collector.get_image(img_size)
            if img_white is not None:
                prediction, chance = model.predict(img_white)
                label = "{}: {:0.2f}%".format(prediction, chance * 100)

                cv2.putText(img, label, (25, 25), cv2.FONT_HERSHEY_SIMPLEX, 1, (255, 255, 255), 2)

                x, y = normalized_position.x * screen_width, normalized_position.y * screen_height
                self.drag_to(x, y)

                if last_gesture != prediction:
                    if prediction == 'b':
                        self.click()
                    elif prediction == 'c':
                        self.right_click()
                
                last_gesture = prediction
            if img is not None:
                cv2.imshow("Image", img)