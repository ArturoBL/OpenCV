import glfw
from OpenGL.GL import *
from OpenGL.GLU import *

if not glfw.init():
    raise Exception("GLFW no pudo inicializar")

window = glfw.create_window(800, 600, "ArUco + OpenGL", None, None)
glfw.make_context_current(window)

glEnable(GL_DEPTH_TEST)

def set_projection_from_camera(K, width, height, near=0.01, far=100.0):
    fx, fy = K[0,0], K[1,1]
    cx, cy = K[0,2], K[1,2]

    glMatrixMode(GL_PROJECTION)
    glLoadIdentity()

    glFrustum(
        -cx * near / fx,
        (width - cx) * near / fx,
        (cy - height) * near / fy,
        cy * near / fy,
        near,
        far
    )

    glMatrixMode(GL_MODELVIEW)