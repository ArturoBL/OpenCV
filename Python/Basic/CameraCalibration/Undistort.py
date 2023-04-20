import cv2
import numpy as np
import pickle

with open('camera_parameters.pkl', 'rb') as archivo:
    cameraparameters = pickle.load(archivo)

cameraMatrix = cameraparameters['Matrix']
dist = cameraparameters['dist']

#Capture image to undistort
cap = cv2.VideoCapture(0,cv2.CAP_DSHOW)     # Device Initialization with directshow
cap.set(cv2.CAP_PROP_FRAME_WIDTH, 640)
cap.set(cv2.CAP_PROP_FRAME_HEIGHT, 480)
cap.set(cv2.CAP_PROP_FPS, 60)
while True:
    _, image = cap.read()
    cv2.imshow("Image Capture", image)
    k = cv2.waitKey(1) & 0xFF
    if k != 255:  # save only images with detected chessboard
        break
cap.release()

h,  w = image.shape[:2]
newcameramtx, roi = cv2.getOptimalNewCameraMatrix(cameraMatrix, dist, (w,h), 1, (w,h))

# undistort
dst = cv2.undistort(image, cameraMatrix, dist, None, newcameramtx)

# crop the image
x, y, w, h = roi
dst = dst[y:y+h, x:x+w]

cv2.imshow("Original", image)
cv2.imshow("Undistort", dst)

while True:
    k = cv2.waitKey(1) & 0xFF
    if k != 255:
        break

cv2.destroyAllWindows()
