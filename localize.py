import cv2
import numpy as np

def detect_forgery_regions(original_img, ela_img, threshold=200):

    img = original_img.copy()

    gray = cv2.cvtColor(ela_img, cv2.COLOR_RGB2GRAY)

    _, thresh = cv2.threshold(gray, threshold, 255, cv2.THRESH_BINARY)

    contours,_ = cv2.findContours(
        thresh,
        cv2.RETR_EXTERNAL,
        cv2.CHAIN_APPROX_SIMPLE
    )

    boxes = []

    for c in contours:

        x,y,w,h = cv2.boundingRect(c)

        if w*h > 500:

            boxes.append((x,y,w,h))

            cv2.rectangle(
                img,
                (x,y),
                (x+w,y+h),
                (255,0,0),
                2
            )

    return img, boxes