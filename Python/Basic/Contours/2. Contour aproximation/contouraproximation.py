import cv2

#Load image
image = cv2.imread('../../../../Media/simplecontour.png')
image2 = image.copy()

#Convert to grayscale
gray = cv2.cvtColor(image, cv2.COLOR_BGR2GRAY)

#Threshold image
ret, thresh = cv2.threshold(gray, 150, 255, cv2.THRESH_BINARY)

#Find contours
contours, _ = cv2.findContours(thresh, cv2.RETR_TREE, cv2.CHAIN_APPROX_NONE)
contourssimple, _ = cv2.findContours(thresh, cv2.RETR_TREE, cv2.CHAIN_APPROX_SIMPLE)

#Draw contours
for contour in contours:
    for point in contour:
        x, y = point[0]
        cv2.circle(image, (x, y), 3, (0, 0, 255), -1)  

#Draw contours for simple approximation
for contour in contourssimple:
    for point in contour:
        x, y = point[0]
        cv2.circle(image2, (x, y), 3, (0, 0, 255), -1)  

cv2.imshow('Image CHAIN_APPROX_NONE', image)
cv2.imshow('Image CHAIN_APPROX_SIMPLE', image2)
cv2.waitKey(0)
cv2.destroyAllWindows()