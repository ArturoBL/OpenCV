import cv2
import cv2.aruco as aruco
import os

diccionario = aruco.getPredefinedDictionary(aruco.DICT_4X4_50)
os.makedirs("markers", exist_ok=True)

for marker_id in range(5):
    img = aruco.generateImageMarker(diccionario, marker_id, 200)
    cv2.imwrite(f"markers/aruco_{marker_id}.png", img)