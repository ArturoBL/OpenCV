import cv2
import cv2.aruco as aruco

# 1. Elegir diccionario
diccionario = aruco.getPredefinedDictionary(aruco.DICT_4X4_50)

# 2. Crear imagen del marker
id_marker = 0
tamano = 200  # pixeles

imagen = aruco.generateImageMarker(diccionario, id_marker, tamano)

# 3. Guardar imagen
cv2.imwrite("aruco_0.png", imagen)
