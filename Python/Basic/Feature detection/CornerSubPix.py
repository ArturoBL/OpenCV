import numpy as np
import cv2

filename = '..\..\..\Media\distort.jpg'
img = cv2.imread(filename)
gray = cv2.cvtColor(img,cv2.COLOR_BGR2GRAY)

# find Harris corners
gray = np.float32(gray)
dst = cv2.cornerHarris(gray,2,3,0.04)
dst = cv2.dilate(dst,None)
ret, dst = cv2.threshold(dst,0.01*dst.max(),255,0)
dst = np.uint8(dst)

# find centroids
ret, labels, stats, centroids = cv2.connectedComponentsWithStats(dst)

# define the criteria to stop and refine the corners
criteria = (cv2.TERM_CRITERIA_EPS + cv2.TERM_CRITERIA_MAX_ITER, 100, 0.001)

# Refine corners to subpixel accuracy
corners = cv2.cornerSubPix(gray, np.float32(centroids), (5, 5), (-1, -1), criteria)

# Draw results on image
img_display = img.copy()

# Draw centroids (before refinement) in blue
for centroid in centroids:
    x, y = int(centroid[0]), int(centroid[1])
    cv2.circle(img_display, (x, y), 3, (255, 0, 0), -1)

# Draw refined corners in green
for corner in corners:
    x, y = int(corner[0]), int(corner[1])
    cv2.circle(img_display, (x, y), 3, (0, 255, 0), -1)

# Display the result
cv2.imshow('Corners: Blue=Centroids, Green=Refined', img_display)
cv2.waitKey(0)
cv2.destroyAllWindows()
