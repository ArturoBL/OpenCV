#Fuente:
#https://www.youtube.com/watch?v=-LqHr5V67C4&ab_channel=HackersRealm
import cv2
from cv2 import dnn_superres

# initialize super resolution object
sr = dnn_superres.DnnSuperResImpl_create()

# link to download model
#https://github.com/Saafke/EDSR_Tensorflow/blob/master/models/

# read the model
path = 'LapSRN_x8.pb'
sr.readModel(path)

# set the model and scale
sr.setModel('lapsrn', 8)

# if you don't have cuda support
#sr.setPreferableBackend(cv2.dnn.DNN_BACKEND_OPENCV )
#sr.setPreferableTarget(cv2.dnn.DNN_TARGET_CPU )

# if you have cuda support
sr.setPreferableBackend(cv2.dnn.DNN_BACKEND_CUDA )
sr.setPreferableTarget(cv2.dnn.DNN_TARGET_CUDA )

# read the image
image = cv2.imread('../../../../Media/Lena.jpg')
imgsize = image.shape[:2]

newSize = (imgsize[0]//3, imgsize[1]//3)
resized_image = cv2.resize(image, newSize)

imgnearest = cv2.resize(resized_image, imgsize, interpolation=cv2.INTER_NEAREST)

cv2.imshow('Original',image)
cv2.imshow('Downscaled',resized_image)
cv2.imshow('Nearest',imgnearest)

# upsample the image
upscaled = sr.upsample(resized_image)
cv2.imshow('Upscaled',upscaled)

#Esperamos a que se presione una tecla
cv2.waitKey()

#Cerramos todas las ventanas creadas
cv2.destroyAllWindows()