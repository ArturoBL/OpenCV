import numpy as np
import cv2
from matplotlib import pyplot as plt

filename = '..\..\..\Media\distort.jpg'
img = cv2.imread(filename)
gray = cv2.cvtColor(img,cv2.COLOR_BGR2GRAY)

corners = cv2.goodFeaturesToTrack(gray,25,0.01,10)
corners = np.int32(corners)

img_display = img.copy()

for corner in corners:
    x, y = int(corner[0][0]), int(corner[0][1])
    cv2.circle(img_display, (x, y), 3, (0, 255, 0), -1)

# Display the result
cv2.imshow('Corners: Blue=Centroids, Green=Refined', img_display)
cv2.waitKey(0)
cv2.destroyAllWindows()