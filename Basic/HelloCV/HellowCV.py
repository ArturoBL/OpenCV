import cv2

#Leemos la imagen
img = cv2.imread('../../media/lena.jpg')

#Mostramos la imagen en una ventana con título "Image"
cv2.imshow('Image',img)

#Esperamos a que se presione una tecla
cv2.waitKey()

#Cerramos todas las ventanas creadas
cv2.destroyAllWindows()