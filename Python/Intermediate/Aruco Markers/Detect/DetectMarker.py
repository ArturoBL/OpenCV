import cv2
import cv2.aruco as aruco

img = cv2.imread("aruco_0.png")

diccionario = aruco.getPredefinedDictionary(aruco.DICT_4X4_50)
detector = aruco.ArucoDetector(diccionario)

corners, ids, _ = detector.detectMarkers(img)

print("IDs detectados:", ids)
