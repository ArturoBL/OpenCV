import cv2
import numpy as np
import pywavefront
import pickle
from packaging import version 

# -----------------------------
# Configuración
# -----------------------------
MARKER_SIZE = 0.10  # 10 cm en metros
OBJ_SCALE = 0.05     # ajusta si el modelo es muy grande/pequeño

# -----------------------------
# Cargar calibración
# -----------------------------
# read camera calibration parameters file (check Basic\CameraCalibration)
with open('../../../../Media/ps3_camera_parameters.pkl', 'rb') as archivo:
    cameraparameters = pickle.load(archivo)
camera_matrix = cameraparameters['Matrix']
dist_coeffs = cameraparameters['dist']


# -----------------------------
# ArUco
# -----------------------------
if version.parse(cv2.__version__) >= version.parse("4.7.0"):
    dictionary = cv2.aruco.getPredefinedDictionary(cv2.aruco.DICT_4X4_250)
    detectorParams = cv2.aruco.DetectorParameters()
    detector = cv2.aruco.ArucoDetector(dictionary, detectorParams)
    
else:
    dictionary = cv2.aruco.Dictionary_get(cv2.aruco.DICT_4X4_250)
    detectorParams = cv2.aruco.DetectorParameters_create()


# -----------------------------
# Cargar modelo OBJ
# -----------------------------
scene = pywavefront.Wavefront(
    "../../../../Media/teddy.obj",
    collect_faces=True
)

vertices = np.array(scene.vertices, dtype=np.float32)
faces = scene.mesh_list[0].faces

# Centrar el modelo en el origen
vertices -= vertices.mean(axis=0)

# Escalar al tamaño del marcador
vertices *= MARKER_SIZE * OBJ_SCALE

vertices[:, [1, 2]] = vertices[:, [2, 1]]
vertices[:, 1] *= -1

# -----------------------------
# Puntos 3D del marcador
# -----------------------------
half = MARKER_SIZE / 2
obj_marker_points = np.array([
    [-half,  half, 0],
    [ half,  half, 0],
    [ half, -half, 0],
    [-half, -half, 0]
], dtype=np.float32)


def translate_vertices(vertices, tx=0, ty=0, tz=0):
    T = np.array([tx, ty, tz], dtype=np.float32)
    return vertices + T

vertices = translate_vertices(vertices, tz=0.1)

#Rotación de vertices en sistema de coordenadas del objeto
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

# -----------------------------
# Webcam
# -----------------------------
cap = cv2.VideoCapture(2, cv2.CAP_V4L2)
cap.set(cv2.CAP_PROP_FRAME_WIDTH, 640)
cap.set(cv2.CAP_PROP_FRAME_HEIGHT, 480)
cap.set(cv2.CAP_PROP_FPS, 150)

while True:
    ret, frame = cap.read()
    if not ret:
        break

    gray = cv2.cvtColor(frame, cv2.COLOR_BGR2GRAY)
    corners, ids, _ = detector.detectMarkers(gray)
    #markerCorners, markerIds, rejectedCandidates = detector.detectMarkers(frame)
    if version.parse(cv2.__version__) >= version.parse("4.7.0"):
        corners, ids, _ = detector.detectMarkers(gray)
    else:
        corners, ids, _ = cv2.aruco.detectMarkers(
            frame, dictionary, parameters=detectorParams)

    if ids is not None:
        #cv2.aruco.drawDetectedMarkers(frame, corners)

        for corner in corners:
            img_points = corner.reshape(4, 2)

            success, rvec, tvec = cv2.solvePnP(
                obj_marker_points,
                img_points,
                camera_matrix,
                dist_coeffs,
                flags=cv2.SOLVEPNP_ITERATIVE
            )

            if not success:
                continue

            # Dibujar ejes del marcador
            cv2.drawFrameAxes(
                frame,
                camera_matrix,
                dist_coeffs,
                rvec,
                tvec,
                MARKER_SIZE * 0.5
            )

            # Proyectar el modelo 3D
            imgpts, _ = cv2.projectPoints(
                vertices,
                rvec,
                tvec,
                camera_matrix,
                dist_coeffs
            )

            imgpts = imgpts.reshape(-1, 2)

            # Dibujar caras (wireframe)
            for face in faces:
                pts = np.array([imgpts[i] for i in face], dtype=np.int32)
                cv2.polylines(frame, [pts], True, (0, 255, 0), 1)

    cv2.imshow("ArUco + OBJ", frame)

    if cv2.waitKey(1) & 0xFF == 27:
        break

cap.release()
cv2.destroyAllWindows()