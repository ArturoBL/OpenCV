import cv2
import numpy as np

# Ensure GPU is available
print(cv2.cuda.getCudaEnabledDeviceCount())

# The prototxt and model need to be downloaded separately
net = cv2.dnn.readNetFromCaffe("../../../../Media/deploy.prototxt.txt", "../../../../Media/res10_300x300_ssd_iter_140000.caffemodel")
net.setPreferableBackend(cv2.dnn.DNN_BACKEND_CUDA)
net.setPreferableTarget(cv2.dnn.DNN_TARGET_CUDA)
# Set CUDA device
cv2.cuda.setDevice(0)

image = cv2.imread('../../../../Media/lena.jpg')

blob = cv2.dnn.blobFromImage(cv2.resize(image, (300, 300)), 1.0,
        (300, 300), (104.0, 177.0, 123.0))
net.setInput(blob)
detections = net.forward()

# The model returns the detections in an odd format a=[:, :, :, :]. 
# Each detection is a[2] while the confidence and bounding box are in 
# a[3]
for i in range(detections.shape[2]):
    confidence = detections[0, 0, i, 2]
    if confidence > 0.3:
        (h, w) = image.shape[:2]
        box = detections[0, 0, i, 3:7] * np.array([w, h, w, h])
        (startX, startY, endX, endY) = box.astype("int")
        cv2.rectangle(image, (startX, startY), (endX, endY),
            (0, 0, 255), 2)
            
cv2.imshow('Image',image)

#Esperamos a que se presione una tecla
cv2.waitKey()

#Cerramos todas las ventanas creadas
cv2.destroyAllWindows()