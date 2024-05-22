import cv2


cap = cv2.VideoCapture("Video2.mp4")

Object_Detector = cv2.createBackgroundSubtractorMOG2(history=200,varThreshold=40)

while True:
    ret, frame = cap.read()

    height,width,_ = frame.shape
    print(height,width)

    roi = frame[:,:]

    mask = Object_Detector.apply(frame)
    _, mask = cv2.threshold(mask, 254,255,cv2.THRESH_BINARY)

    contours, _ = cv2.findContours(mask,cv2.RETR_TREE,cv2.CHAIN_APPROX_SIMPLE)

    for cnt in contours:
        #calculating area and removing small elements
        area = cv2.contourArea(cnt)
        if area>100:

            x,y,w,h = cv2.boundingRect(cnt)
            cv2.rectangle(roi, (x,y), (x+w,y+h), (255,0,0),3)
            #cv2.drawContours(frame,[cnt],-1,(255,0,0),3)


    cv2.imshow("Frame",frame)
    cv2.imshow("mask", mask)
    #cv2.imshow("Frame", roi)

    key = cv2.waitKey(1)
    if key == 20:
        break
cap.release()
cap.destroyAllWindows()

