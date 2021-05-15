import numpy as np
import cv2

cap = cv2.VideoCapture('calle.mp4')

while(cap.isOpened()):
    ret, frame = cap.read()
    img = cv2.resize(frame,(640,360),interpolation = cv2.INTER_LANCZOS4)
    #gray = cv2.cvtColor(frame, cv2.COLOR_BGR2GRAY)

    cv2.imshow('frame',img)
    if cv2.waitKey(1) & 0xFF == 27:
        break

cap.release()
cv2.destroyAllWindows()