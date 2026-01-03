import cv2
import numpy as np
import pickle

# read camera calibration parameters file (check Basic\CameraCalibration)
with open('camera_parameters.pkl', 'rb') as archivo:
    cameraparameters = pickle.load(archivo)
cameraMatrix = cameraparameters['Matrix']
dist = cameraparameters['dist']

#Aruco detector setup
dictionary = cv2.aruco.getPredefinedDictionary(cv2.aruco.DICT_4X4_250)
parameters = cv2.aruco.DetectorParameters()
detector = cv2.aruco.ArucoDetector(dictionary, parameters)
# Marker size (meters)
marker_length = 0.1
half = marker_length / 2

object_points = np.array([
    [-half,  half, 0],
    [ half,  half, 0],
    [ half, -half, 0],
    [-half, -half, 0]
], dtype=np.float32)

def pose_esitmation(frame):
    markerCorners, markerIds, rejectedCandidates = detector.detectMarkers(frame)
    if markerIds is not None:
        cv2.aruco.drawDetectedMarkers(frame, markerCorners, markerIds)
        for i in range(len(markerIds)):
            image_points = markerCorners[i][0].astype(np.float32)

            # tvec = marker position relative to camera
            # rvec = marker orientation relative to camera
            success, rvec, tvec = cv2.solvePnP(
                object_points,
                image_points,
                cameraMatrix,
                dist,
                flags=cv2.SOLVEPNP_IPPE_SQUARE
            )

            if success:
                cv2.drawFrameAxes(
                    frame,
                    cameraMatrix,
                    dist,
                    rvec,
                    tvec,
                    0.09
                )
                
    return frame

cap = cv2.VideoCapture(1)
while True:
    ret, frame = cap.read()
    if not ret:
        break

    output = pose_esitmation(frame)

    cv2.imshow('ArUco Detector', output)
    if cv2.waitKey(1) & 0xFF == 27:
        break

cap.release()
cv2.destroyAllWindows()