import cv2
import glfw
import numpy as np
from OpenGL.GL import *
from OpenGL.GLU import *
import pywavefront
import pickle
from packaging import version 

# ============================================================
# CONFIGURACIÓN
# ============================================================
WIDTH, HEIGHT = 640, 480
MARKER_SIZE = 0.10  # metros (10 cm)
OBJ_SCALE = 0.05     # ajusta si el modelo es muy grande/pequeño


# -----------------------------
# Cargar calibración
# -----------------------------
# read camera calibration parameters file (check Basic\CameraCalibration)
with open('camera_parameters.pkl', 'rb') as archivo:
    cameraparameters = pickle.load(archivo)
camera_matrix = cameraparameters['Matrix']
dist_coeffs = cameraparameters['dist']

# ============================================================
# OPENGL / GLFW
# ============================================================
if not glfw.init():
    raise RuntimeError("No se pudo inicializar GLFW")

window = glfw.create_window(WIDTH, HEIGHT, "ArUco + OpenGL AR", None, None)
glfw.make_context_current(window)

glEnable(GL_DEPTH_TEST)
glEnable(GL_BLEND)
glBlendFunc(GL_SRC_ALPHA, GL_ONE_MINUS_SRC_ALPHA)
glPolygonMode(GL_FRONT_AND_BACK, GL_LINE)
glLineWidth(1.5)

# ============================================================
# PROYECCIÓN OPENGL DESDE CÁMARA REAL
# ============================================================
def set_projection_from_camera(K, width, height, near=0.01, far=5.0):
    fx, fy = K[0,0], K[1,1]
    cx, cy = K[0,2], K[1,2]

    glMatrixMode(GL_PROJECTION)
    glLoadIdentity()

    glFrustum(
        -cx * near / fx,
        (width - cx) * near / fx,
        -(height - cy) * near / fy,
        cy * near / fy,
        near,
        far
    )

    glMatrixMode(GL_MODELVIEW)

set_projection_from_camera(camera_matrix, WIDTH, HEIGHT)

# ============================================================
# CONVERSIÓN POSE OPENCV → OPENGL
# ============================================================
def cv_to_gl_pose(rvec, tvec):
    R, _ = cv2.Rodrigues(rvec)

    M = np.eye(4, dtype=np.float32)
    M[:3, :3] = R
    M[:3, 3] = tvec[:, 0]

    # OpenCV → OpenGL (invertir Y y Z)
    flip = np.diag([1, -1, -1, 1])
    M = flip @ M

    return M.T  # column-major

# ============================================================
# CARGAR MODELO OBJ
# ============================================================
scene = pywavefront.Wavefront("../../../../Media/teddy.obj", collect_faces=True)
vertices = np.array(scene.vertices, dtype=np.float32)
faces = scene.mesh_list[0].faces

vertices = np.array(scene.vertices, dtype=np.float32)
faces = scene.mesh_list[0].faces

# Centrar el modelo en el origen
vertices -= vertices.mean(axis=0)

# Escalar al tamaño del marcador
vertices *= MARKER_SIZE * OBJ_SCALE

vertices[:, [1, 2]] = vertices[:, [2, 1]]   #intercambiar Y y Z
vertices[:, 1] *= -1                     #invertir Y

def translate_vertices(vertices, tx=0, ty=0, tz=0):
    T = np.array([tx, ty, tz], dtype=np.float32)
    return vertices + T

# Elevar el modelo para que "descanse" sobre el marcador
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


# ============================================================
# DIBUJAR OBJ
# ============================================================
def draw_obj(vertices, faces):
    glColor4f(0.0, 1.0, 0.0, 0.5)

    glBegin(GL_TRIANGLES)
    for face in faces:
        for idx in face:
            glVertex3fv(vertices[idx])
    glEnd()

# ============================================================
# DIBUJAR BACKGROUND (VIDEO)
# ============================================================
def draw_background(frame):
    frame = cv2.flip(frame, 0)
    frame = cv2.cvtColor(frame, cv2.COLOR_BGR2RGB)

    glDisable(GL_DEPTH_TEST)
    glDrawPixels(
        frame.shape[1],
        frame.shape[0],
        GL_RGB,
        GL_UNSIGNED_BYTE,
        frame
    )
    glEnable(GL_DEPTH_TEST)

# ============================================================
# ARUCO
# ============================================================
if version.parse(cv2.__version__) >= version.parse("4.7.0"):
    dictionary = cv2.aruco.getPredefinedDictionary(cv2.aruco.DICT_4X4_250)
    detectorParams = cv2.aruco.DetectorParameters()
    detector = cv2.aruco.ArucoDetector(dictionary, detectorParams)
    
else:
    dictionary = cv2.aruco.Dictionary_get(cv2.aruco.DICT_4X4_250)
    detectorParams = cv2.aruco.DetectorParameters_create()

half = MARKER_SIZE / 2
obj_points = np.array([
    [-half,  half, 0],
    [ half,  half, 0],
    [ half, -half, 0],
    [-half, -half, 0]
], dtype=np.float32)

# ============================================================
# WEBCAM
# ============================================================
cap = cv2.VideoCapture(2, cv2.CAP_V4L2)
cap.set(cv2.CAP_PROP_FRAME_WIDTH, 640)
cap.set(cv2.CAP_PROP_FRAME_HEIGHT, 480)
cap.set(cv2.CAP_PROP_FPS, 75)

# ============================================================
# LOOP PRINCIPAL
# ============================================================
while not glfw.window_should_close(window):
    ret, frame = cap.read()
    if not ret:
        break

    gray = cv2.cvtColor(frame, cv2.COLOR_BGR2GRAY)
    if version.parse(cv2.__version__) >= version.parse("4.7.0"):
        corners, ids, _ = detector.detectMarkers(gray)
    else:
        corners, ids, _ = cv2.aruco.detectMarkers(
            frame, dictionary, parameters=detectorParams)

    glClear(GL_COLOR_BUFFER_BIT | GL_DEPTH_BUFFER_BIT)
    draw_background(frame)

    if ids is not None:
        for corner in corners:
            success, rvec, tvec = cv2.solvePnP(
                obj_points,
                corner.reshape(4, 2),
                camera_matrix,
                dist_coeffs,
                flags=cv2.SOLVEPNP_ITERATIVE
            )

            if success:
                glLoadIdentity()
                glLoadMatrixf(cv_to_gl_pose(rvec, tvec))
                draw_obj(vertices, faces)

    glfw.swap_buffers(window)
    glfw.poll_events()

# ============================================================
# CLEANUP
# ============================================================
cap.release()
glfw.terminate()
