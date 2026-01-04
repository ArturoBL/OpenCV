import cv2
import numpy as np
import pickle

# read camera calibration parameters file (check Basic\CameraCalibration)
with open('camera_parameters.pkl', 'rb') as archivo:
    cameraparameters = pickle.load(archivo)
cameraMatrix = cameraparameters['Matrix']
dist = cameraparameters['dist']

aruco_dict = cv2.aruco.getPredefinedDictionary(cv2.aruco.DICT_4X4_50)
parameters = cv2.aruco.DetectorParameters()
detector = cv2.aruco.ArucoDetector(aruco_dict, parameters)

MARKER_SIZE = 0.10  # 10 cm (en metros)

half = MARKER_SIZE / 2
object_points = np.array([
    [-half,  half, 0],
    [ half,  half, 0],
    [ half, -half, 0],
    [-half, -half, 0]
], dtype=np.float32)

distance = 0.0
z_distance = 0.0

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
                    0.03
                )
                distance = np.linalg.norm(tvec)
                print("Distance to marker:", distance, "meters")
                #z_distance = tvec[2][0]
                #print(f"Distancia frontal (Z): {z_distance:.3f} metros")
                #Z es la distancia perpendicular al plano de la cámara.
    return frame

cap = cv2.VideoCapture(0)
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