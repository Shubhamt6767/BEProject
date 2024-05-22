import cv2
import imutils
from RealtimeObjectDetection import Detector
#img = cv2.imread('Rohit.jpg')
def PedestrianDetection(file):

    cap = cv2.VideoCapture(file)
    while True:
        ret, frame = cap.read()
        frame = imutils.resize(frame, width=1600)
        frame = Detector(frame)
        k = cv2.waitKey(30) & 0xff
        if k == 27:
            break
    cv2.destroyAllWindows()
file = "video_0016.mp4"
PedestrianDetection(file)

