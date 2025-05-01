import cv2
import numpy as np

#Leemos la imagen original
img = cv2.imread('../../../media/lena.jpg')

#Obtenemos sus dimensiones y recortamos el array para trabajar con las dimensiones
#Originalmente es de 3 dimensiones (altura, ancho, canales)
#El array resultante es de 2 dimensiones (altura, ancho)
imgsize = img.shape[:2]

#Redimensionamos la imagen a 1/3
newSize = (imgsize[0]//3, imgsize[1]//3)
resized_image = cv2.resize(img, newSize)

#Realizamos las interpolaciones
'''
enum  	cv::InterpolationFlags {
  cv::INTER_NEAREST = 0,
  cv::INTER_LINEAR = 1,
  cv::INTER_CUBIC = 2,
  cv::INTER_AREA = 3,
  cv::INTER_LANCZOS4 = 4,
  cv::INTER_LINEAR_EXACT = 5,
  cv::INTER_NEAREST_EXACT = 6,
  cv::INTER_MAX = 7,
  cv::WARP_FILL_OUTLIERS = 8,
  cv::WARP_INVERSE_MAP = 16
}'''
imglanczos = cv2.resize(resized_image, imgsize, interpolation=cv2.INTER_LANCZOS4)
imgnearest = cv2.resize(resized_image, imgsize, interpolation=cv2.INTER_NEAREST)
imgbilinear = cv2.resize(resized_image, imgsize, interpolation=cv2.INTER_LINEAR)
imgbicubic = cv2.resize(resized_image, imgsize, interpolation=cv2.INTER_CUBIC)
imgarea = cv2.resize(resized_image, imgsize, interpolation=cv2.INTER_AREA)

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