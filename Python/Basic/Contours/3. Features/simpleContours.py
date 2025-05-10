import cv2

#Load image
image = cv2.imread('../../../../Media/rotatedrect.png')

#Convert to grayscale
gray = cv2.cvtColor(image, cv2.COLOR_BGR2GRAY)

#Threshold image
ret, thresh = cv2.threshold(gray, 150, 255, cv2.THRESH_BINARY)

#Find contours
contours, hierarchy = cv2.findContours(thresh, cv2.RETR_TREE, cv2.CHAIN_APPROX_NONE)

#Draw contours
cv2.drawContours(image, contours, -1, (0, 255, 0), 3)

contour = contours[0]

M = cv2.moments(contour)
area = cv2.contourArea(contour)
center = (M["m10"] / M["m00"], M["m01"] / M["m00"])
perimeter = cv2.arcLength(contour, True)

print("Moments: ")
print(M)

print("Area: ", area)
print("Center: ", center)
cv2.circle(image, (int(center[0]), int(center[1])), 5, (0, 0, 255), -1)
print("Perimeter: ", perimeter)

extLeft = tuple(contour[contour[:, :, 0].argmin()][0])
extRight = tuple(contour[contour[:, :, 0].argmax()][0])
extTop = tuple(contour[contour[:, :, 1].argmin()][0])
extBot = tuple(contour[contour[:, :, 1].argmax()][0])
cv2.circle(image, extLeft, 8, (0, 0, 255), -1)
cv2.circle(image, extRight, 8, (0, 255, 0), -1)
cv2.circle(image, extTop, 8, (255, 0, 0), -1)
cv2.circle(image, extBot, 8, (255, 255, 0), -1)

cv2.imshow('Image', image)
cv2.waitKey(0)
cv2.destroyAllWindows()