import cv2
import numpy as np


# 1. Define the dictionary of markers to use
dictionary = cv2.aruco.getPredefinedDictionary(cv2.aruco.DICT_4X4_250)

# 2. Define detection parameters (using defaults here)
parameters = cv2.aruco.DetectorParameters()

# 3. Create the ArucoDetector object
detector = cv2.aruco.ArucoDetector(dictionary, parameters)

# 4. Read image
image = cv2.imread('aruco_0.png')

# 5. Detect the markers
markerCorners, markerIds, rejectedCandidates = detector.detectMarkers(image)
# 6. Process the results (e.g., draw bounding boxes)
if markerIds is not None:
    cv2.aruco.drawDetectedMarkers(image, markerCorners, markerIds)
print(markerIds)

cv2.imshow('ArUco Detector', image)
while True:
    if cv2.waitKey(1) & 0xFF == 27:
        break

cv2.destroyAllWindows()