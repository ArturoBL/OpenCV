import cv2

image = cv2.imread('../../../../Media/contourshierarchy.png')
gray = cv2.cvtColor(image, cv2.COLOR_BGR2GRAY)
ret, thresh = cv2.threshold(gray, 150, 255, cv2.THRESH_BINARY)

contours, hierarchy = cv2.findContours(thresh, cv2.RETR_TREE, cv2.CHAIN_APPROX_NONE)
print("Contours: ",hierarchy.shape[1])
print("Hierarchy: [Next, Previous, First_Child, Parent]")
print(hierarchy)

for i, contour in enumerate(contours):
    cv2.drawContours(image, contour, -1, (0, 255, 0), 2, cv2.LINE_AA)
    area = cv2.contourArea(contour)
    print(f"Area {i}: ", area)
    x, y, w, h = cv2.boundingRect(contour)
    h = hierarchy[0][i][3]
    if h == -1:
        text = str(i) + ' parent '    
    else:
        text = str(i) + ' child, parent: ' + str(h)
    cv2.putText(image, text, (x, y - 5), cv2.FONT_HERSHEY_SIMPLEX, 0.6, (0, 0, 255), 2)
    
cv2.imshow('Image',image)

cv2.waitKey()
cv2.destroyAllWindows()