import cv2
import numpy as np
from pyzbar.pyzbar import decode

#img = cv2.imread('IMG_20200426_140601.jpg')
cap = cv2.VideoCapture(0, cv2.CAP_DSHOW)
cap.set(3,1024)
cap.set(4,768)

while True:
    success, img = cap.read()
    for barcode in decode(img):
        print(barcode.data)
        pts = np.array([barcode.polygon],np.int32)
        pts = pts.reshape((-1,1,2))
        cv2.polylines(img,[pts],True,(255,0,255),5)


    cv2.imshow('Result',img)
    if cv2.waitKey(1) & 0xFF == 27:
        break
cap.release()
cv2.destroyAllWindows()