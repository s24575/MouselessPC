import pyautogui


class GestureService:

    # Class create as mock.
    # In future will be replaced or rebuild
    def __init__(self):
        self.gestures = {'up': 1, 'down': 2, 'left': 3, 'right': 4}

    def process_gestures(self, signal):
        mouse_speed = 30
        response = self.gestures.get(signal)
        match response:
            case 1:
                pyautogui.moveRel(0, -mouse_speed)
            case 2:
                pyautogui.moveRel(0, mouse_speed)
            case 3:
                pyautogui.moveRel(-mouse_speed, 0)
            case 4:
                pyautogui.moveRel(mouse_speed, 0)