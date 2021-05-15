import numpy as np
import cv2

cap = cv2.VideoCapture('../../Media/video.mp4')

while(cap.isOpened()):
    ret, frame = cap.read()

    if ret:
        cv2.imshow('frame',frame)
    else:
        break
    if cv2.waitKey(1) & 0xFF == 27:
        break

cap.release()
cv2.destroyAllWindows()