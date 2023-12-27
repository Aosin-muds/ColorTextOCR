
import cv2
import numpy as np
from PIL import Image
import pytesseract
import matplotlib.pyplot as plt

class TextRectangler:
    def __init__(self, x_threshold=10, y_threshold=10):
        self.x_threshold = x_threshold
        self.y_threshold = y_threshold

    def merge_close_boxes(self, boxes):
        merged_boxes = []
        while boxes:
            box = boxes.pop(0)
            x, y, w, h = box
            close_boxes = [b for b in boxes if (abs(b[0] - x) <= self.x_threshold and abs(b[1] - y) <= self.y_threshold)]
            for b in close_boxes:
                boxes.remove(b)
            for b in close_boxes:
                bx, by, bw, bh = b
                x = min(x, bx)
                y = min(y, by)
                w = max(x + w, bx + bw) - x
                h = max(y + h, by + bh) - y
            merged_boxes.append((x, y, w, h))
        return merged_boxes

    def process_image(self, image_path):
        image = Image.open(image_path)
        image_cv = cv2.cvtColor(np.array(image), cv2.COLOR_RGB2BGR)
        d = pytesseract.image_to_data(image, lang='jpn', output_type=pytesseract.Output.DICT)
        extracted_text = pytesseract.image_to_string(image, lang='jpn')
        boxes = []
        for i in range(len(d['level'])):
            if d['text'][i].strip():
                (x, y, w, h) = (d['left'][i], d['top'][i], d['width'][i], d['height'][i])
                boxes.append((x, y, w, h))
        merged_boxes = self.merge_close_boxes(boxes)
        for box in merged_boxes:
            x, y, w, h = box
            cv2.rectangle(image_cv, (x, y), (x + w, y + h), (0, 255, 0), 2)
        plt.imshow(cv2.cvtColor(image_cv, cv2.COLOR_BGR2RGB))
        plt.axis('off')
        plt.show()
        return extracted_text
