import cv2
import numpy as np

#Leemos la imagen original
img = cv2.imread('../../../media/lena.jpg')
imgsize = img.shape

#Redimensionamos la imagen a 1/3
newSize = (imgsize[1]//3, imgsize[0]//3)
resized_image = cv2.resize(img, newSize)

#Calculamos el tamaño de la imagen redimensionada
newsize = resized_image.shape
fullsize = (newSize[1]*3, newSize[0]*3) 

#Realizamos las interpolaciones
imglanczos = cv2.resize(resized_image, fullsize, interpolation=cv2.INTER_LANCZOS4)
imgnearest = cv2.resize(resized_image, fullsize, interpolation=cv2.INTER_NEAREST)
imgbilinear = cv2.resize(resized_image, fullsize, interpolation=cv2.INTER_LINEAR)
imgbicubic = cv2.resize(resized_image, fullsize, interpolation=cv2.INTER_CUBIC)
imgarea = cv2.resize(resized_image, fullsize, interpolation=cv2.INTER_AREA)

#Mostramos la imagen original
cv2.imshow('Original',img)

#Mostramos las imágenes reescaladas
cv2.imshow('Resized',resized_image)
cv2.imshow('Lanczos',imglanczos)
cv2.imshow('Nearest',imgnearest)
cv2.imshow('Bilinear',imgbilinear)
cv2.imshow('Bicubic',imgbicubic)
cv2.imshow('Area',imgarea)

#Esperamos a que se presione una tecla
cv2.waitKey()

#Cerramos todas las ventanas creadas
cv2.destroyAllWindows()