import cv2
from cvzone.HandTrackingModule import HandDetector
import numpy as np

img_size = 256

def get_hand_bbox_coordinates(hand_x, hand_y, hand_width, hand_height, img_width, img_height, padding: int = 0):
    x1 = max(hand_x - padding, 0)
    x2 = min(hand_x + hand_width + padding, img_width)
    y1 = max(hand_y - padding, 0)
    y2 = min(hand_y + hand_height + padding, img_height)
    return x1, x2, y1, y2


def main():
    # cap = cv2.VideoCapture("http://192.168.0.147:4747/video")
    cap = cv2.VideoCapture(0)
    detector = HandDetector(maxHands=1)
 
    while True:
        success, img = cap.read()
        img_height, img_width, _ = img.shape  
        hands, img = detector.findHands(img)
        if hands:
            hand = hands[0]
            x, y, w, h = hand['bbox']
            x1, x2, y1, y2 = get_hand_bbox_coordinates(x, y, w, h, img_height, img_width, 30)
            crop_width, crop_height = x2 - x1, y2 - y1
            # print(f"x:{x}, y:{y}, w:{w}, h:{h}")
            # print(f"x1:{x1}, x2:{x2}, y1:{y1}, y2:{y2}")

            if crop_width > 0 and crop_height > 0:
                img_crop = img[y1:y2, x1:x2]

                # print(crop_width, crop_height)
                max_length = max(crop_width, crop_height)
                scale_ratio = img_size / max_length

                crop_width = int(crop_width * scale_ratio)
                crop_height = int(crop_height * scale_ratio)

                # print(crop_width, crop_height, scale_ratio)
                img_resized = cv2.resize(img_crop, (crop_width, crop_height))

                img_white = np.ones((img_size, img_size, 3), np.uint8) * 255
                img_white[0:crop_height, 0:crop_width] = img_resized[0:crop_height, 0:crop_width]

                cv2.imshow("Image crop", img_crop)
                cv2.imshow("Image white", img_white)

        cv2.imshow("Image", img)
        if cv2.waitKey(1) == ord("q"):
            break

    cap.release()
    cv2.destroyAllWindows()


if __name__ == '__main__':
    main()
