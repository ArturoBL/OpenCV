import cv2

#Load image
image = cv2.imread('../../../../Media/contours.png')

#Convert to grayscale
gray = cv2.cvtColor(image, cv2.COLOR_BGR2GRAY)

#Threshold image
ret, thresh = cv2.threshold(gray, 150, 255, cv2.THRESH_BINARY)

#Find contours
contours, hierarchy = cv2.findContours(thresh, cv2.RETR_TREE, cv2.CHAIN_APPROX_NONE)

#Draw contours
cv2.drawContours(image, contours, -1, (0, 255, 0), 3)

cv2.imshow('Image', image)
cv2.waitKey(0)
cv2.destroyAllWindows()