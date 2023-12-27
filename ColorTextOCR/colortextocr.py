
import numpy as np
import cv2
from PIL import Image
import matplotlib.pyplot as plt

class Colortextocr:
    def __init__(self):
        self.lower_rgb = None
        self.upper_rgb = None

    def set_color_range(self, lower_rgb, upper_rgb):
        self.lower_rgb = np.array(lower_rgb, dtype=np.uint8)
        self.upper_rgb = np.array(upper_rgb, dtype=np.uint8)

    def extract_color(self, image_cv):
        mask = cv2.inRange(image_cv, self.lower_rgb, self.upper_rgb)
        return cv2.bitwise_and(image_cv, image_cv, mask=mask)

    def convert_to_binary(self, color_image):
        gray_image = cv2.cvtColor(color_image, cv2.COLOR_BGR2GRAY)
        _, binary_image = cv2.threshold(gray_image, 1, 255, cv2.THRESH_BINARY)
        return binary_image

    def save_image(self, image, path):
        cv2.imwrite(path, image)
        print(f"Image saved as {path}")

    def draw_rectangles(self, binary_image, original_image):
        contours, _ = cv2.findContours(binary_image, cv2.RETR_EXTERNAL, cv2.CHAIN_APPROX_SIMPLE)
        for contour in contours:
            x, y, w, h = cv2.boundingRect(contour)
            cv2.rectangle(original_image, (x, y), (x + w, y + h), (0, 255, 0), 2)
        return original_image
