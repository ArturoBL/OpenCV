import cv2 as cv
import numpy as np
import time

image = cv.imread('../../../Media/lena.jpg')

cv.imshow('lena', image)

for_image = np.zeros(image.shape, image.dtype)

alpha = 1.0  # Simple contrast control  [1.0-3.0]
beta = 80    # Simple brightness control [0-100]


# using for loops to access image pixels slow method about 25 seconds
start = time.time()
for y in range(image.shape[0]):
    for x in range(image.shape[1]):
        for c in range(image.shape[2]):
            for_image[y, x, c] = np.clip(alpha*image[y, x, c] + beta, 0, 255)
end = time.time()
seconds = end - start
print("Tiempo for : {0} segundos".format(seconds))
cv.imshow('for image', for_image)

# using convertScaleAbs fast method about 1 millisecond
start = time.time()
fun_image = cv.convertScaleAbs(image, alpha=alpha, beta=beta)
end = time.time()
seconds = end - start
print("Tiempo function : {0} segundos".format(seconds))
cv.imshow('new image', fun_image)

cv.waitKey(0)
cv.destroyAllWindows()
