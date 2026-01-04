import cv2
import numpy as np
import pickle
import pywavefront

# read camera calibration parameters file (check Basic\CameraCalibration)
with open('camera_parameters.pkl', 'rb') as archivo:
    cameraparameters = pickle.load(archivo)
cameraMatrix = cameraparameters['Matrix']
dist = cameraparameters['dist']

aruco_dict = cv2.aruco.getPredefinedDictionary(cv2.aruco.DICT_4X4_50)
parameters = cv2.aruco.DetectorParameters()
detector = cv2.aruco.ArucoDetector(aruco_dict, parameters)

MARKER_SIZE = 0.10  # 10 cm (en metros)
OBJ_SCALE = 0.3

# -----------------------------
# Cargar modelo OBJ
# -----------------------------
scene = pywavefront.Wavefront(
    "teapot.obj",
    collect_faces=True
)

vertices = np.array(scene.vertices, dtype=np.float32)
faces = scene.mesh_list[0].faces

# Centrar el modelo en el origen
vertices -= vertices.mean(axis=0)

# Escalar al tamaño del marcador
vertices *= MARKER_SIZE * OBJ_SCALE

def rotate_vertices(vertices, angle_deg, axis='x'):
    angle = np.deg2rad(angle_deg)
    c, s = np.cos(angle), np.sin(angle)

    if axis == 'x':
        R = np.array([
            [1, 0,  0],
            [0, c, -s],
            [0, s,  c]
        ])
    elif axis == 'y':
        R = np.array([
            [ c, 0, s],
            [ 0, 1, 0],
            [-s, 0, c]
        ])
    elif axis == 'z':
        R = np.array([
            [c, -s, 0],
            [s,  c, 0],
            [0,  0, 1]
        ])
    return vertices @ R.T

def translate_vertices(vertices, tx=0, ty=0, tz=0):
    T = np.array([tx, ty, tz], dtype=np.float32)
    return vertices + T

vertices = rotate_vertices(vertices, 90, 'x')
vertices = translate_vertices(vertices, tz=MARKER_SIZE / 2)

half = MARKER_SIZE / 2
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
                    0.03
                )
                
                # Proyectar el modelo 3D
                imgpts, _ = cv2.projectPoints(
                    vertices,
                    rvec,
                    tvec,
                    cameraMatrix,
                    dist
                )

                imgpts = imgpts.reshape(-1, 2)

                # Dibujar caras (wireframe)
                for face in faces:
                    pts = np.array([imgpts[i] for i in face], dtype=np.int32)
                    cv2.polylines(frame, [pts], True, (0, 255, 0), 1)
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