# Ejemplo de como usar cámara móvil Android desde OpenCV
#
# Descargar e instalar en Android IP Webcam
# Configurar la resolución y calidad de video para mejorar la velocidad de transmisión
# Iniciar servidor
# Copiar la dirección IP del servicio
# Modificar la dirección URL en el código


import requests
import cv2
import numpy as np

  
#Modificar aquí la dirección del servicio
url = "http://192.168.100.65:8080/shot.jpg"
  

while True:
    img_resp = requests.get(url)
    img_arr = np.array(bytearray(img_resp.content), dtype=np.uint8)
    img = cv2.imdecode(img_arr, -1)

    # width = int(img.shape[1] * 50 / 100)
    # height = int(img.shape[0] * 50 / 100)
    # dsize = (width, height)
    # output = cv2.resize(img, dsize)
    # cv2.imshow("Android_cam", img)

    cv2.imshow("Android_cam", img)
  
    # Press Esc key to exit
    if cv2.waitKey(1) == 27:
        break
  
cv2.destroyAllWindows()
