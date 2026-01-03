import cv2
import numpy as np

# 1. Define the dictionary of markers to use
dictionary = cv2.aruco.getPredefinedDictionary(cv2.aruco.DICT_4X4_250)

# 2. Define detection parameters (using defaults here)
parameters = cv2.aruco.DetectorParameters()

# 3. Create the ArucoDetector object
detector = cv2.aruco.ArucoDetector(dictionary, parameters)

# 4. Load or capture an image (example with a placeholder)
# frame = cv.imread('path_to_your_image.png')
# Placeholder for image acquisition, e.g., from a webcam:
cap = cv2.VideoCapture(1)
while True:
    ret, frame = cap.read()
    if not ret:
        break

    # 5. Detect the markers
    markerCorners, markerIds, rejectedCandidates = detector.detectMarkers(frame)

    # 6. Process the results (e.g., draw bounding boxes)
    if markerIds is not None:
        cv2.aruco.drawDetectedMarkers(frame, markerCorners, markerIds)
        # Further processing for pose estimation can go here

    # Display the image
    cv2.imshow('ArUco Detector', frame)
    if cv2.waitKey(1) & 0xFF == 27:
        break

cap.release()
cv2.destroyAllWindows()