import cv2

#Load image
image = cv2.imread('../../../../Media/10002EM.png')
image2 = image.copy()

#Invert image to find the white parts
inv = (255-image)

#Apply threshold
gray = cv2.cvtColor(inv, cv2.COLOR_BGR2GRAY)
ret, thresh = cv2.threshold(gray, 150, 255, cv2.THRESH_BINARY)

#Find contour vertices through simple approximation
contourssimple, _ = cv2.findContours(thresh, cv2.RETR_TREE, cv2.CHAIN_APPROX_SIMPLE)

#Draw contours vertex for simple approximation
for contour in contourssimple:
    for point in contour:
        x, y = point[0]
        cv2.circle(image, (x, y), 3, (0, 0, 255), -1)  

#Find contour vertices with none approximation with higher number of vertices to reduce
contours, _ = cv2.findContours(thresh, cv2.RETR_TREE, cv2.CHAIN_APPROX_NONE)

epsilon=0.001
for contour in contours:
    approx = cv2.approxPolyDP(contour, epsilon * cv2.arcLength(contour, True), True)
    ctm = approx.reshape(-1, 2)
    for (x, y) in ctm:
        cv2.circle(image2, (x, y), 1, (0, 0, 255), 3)

cv2.imshow('Image CHAIN_APPROX_SIMPLE', image)
cv2.imshow('Image AproxPolyDP', image2)
cv2.waitKey(0)
cv2.destroyAllWindows()