#Crop Image
import cv2

img = cv2.imread('../../../Media/lena.jpg')
x = 223
y = 209
w = 157
h = 157
x2 = x + w
y2 = y + h
crop = img[y:y2, x:x2]

cv2.imshow('image',img)
cv2.imshow('crop',crop)

cv2.waitKey(0)
cv2.destroyAllWindows()