import cv2
import time

cap = cv2.VideoCapture(0, cv2.CAP_DSHOW)

#Configuramos captura de video
cap.set(cv2.CAP_PROP_FRAME_WIDTH,320)
cap.set(cv2.CAP_PROP_FRAME_HEIGHT,240)
cap.set(cv2.CAP_PROP_FPS, 60)

#Obtenemos y mostramos la capacidad de FPS del dispositivo
fps = cap.get(cv2.CAP_PROP_FPS)
print("FPS usando video.get(cv2.CAP_PROP_FPS) : {0}".format(fps))

#Número de frames a capturar:
num_frames = 240
print("Capturando {0} frames...".format(num_frames))

#Iniciamos la captura y el conteo de tiempo
start = time.time()
for i in range(0, num_frames):
    ret, frame = cap.read()
end = time.time()

#Calulamos y mostramos FPS
seconds = end - start
print ("Tiempo total : {0} segundos".format(seconds))
fps  = num_frames / seconds
print("FPS estimado: {0}".format(fps))

cap.release()