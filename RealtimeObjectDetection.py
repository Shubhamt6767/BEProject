import cv2
import numpy as np
from imutils.object_detection import non_max_suppression

HOGCV = cv2.HOGDescriptor()

HOGCV.setSVMDetector(cv2.HOGDescriptor_getDefaultPeopleDetector())
fgbg = cv2.createBackgroundSubtractorMOG2()

prev_centroid = None
pedestrians = []


def Detector(frame):
    rects, weight = HOGCV.detectMultiScale(frame, winStride=(4, 4), padding=(8, 8), scale=1.03)
    # applying the rectangle
    rects = np.array([[x, y, x + w, y + h] for (x, y, w, h) in rects])

    pick = non_max_suppression(rects, probs=None, overlapThresh=0.65)
    c = 1
    gray = cv2.cvtColor(frame, cv2.COLOR_BGR2GRAY)
    fgmask = fgbg.apply(gray)

    thresh = cv2.threshold(fgmask, 128, 255, cv2.THRESH_BINARY)[1]

    for x, y, w, h in pick:
        cv2.rectangle(frame, (x, y), (w, h), (0, 255, 0), 2)
        cv2.rectangle(frame, (x, y - 20), (w, y), (0, 255, 0), -1)
        cv2.putText(frame, f'Pedestrian: {c}', (x, y), cv2.FONT_HERSHEY_SIMPLEX, 0.6, (255, 255, 255), 2)
        c += 1
    cv2.putText(frame, f'Total Person : {c - 1}', (20, 430), cv2.FONT_HERSHEY_SIMPLEX, 0.6, (255, 255, 255), 2)
    cv2.imshow('output', frame)
    return frame
