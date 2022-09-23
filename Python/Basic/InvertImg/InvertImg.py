#Invert Image
import cv2

img = cv2.imread('../../../Media/lena.jpg')
img = (255-img)
cv2.imshow('Inverted image',img)

cv2.waitKey(0)
cv2.destroyAllWindows()