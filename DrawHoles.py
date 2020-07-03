import cv2

#read binary image
img = cv2.imread('holes.png')

#Extract any channel since it's already a binary image
bw,_,_ = cv2.split(img)
#bw = img[:,:,0]

contours, hierarchy = cv2.findContours(bw, cv2.RETR_TREE, cv2.CHAIN_APPROX_SIMPLE )
# hierarchy description : [Next, Previous, First_Child, Parent]

cn = 0      #contour index

for cnt in contours:

    # We consider a hole a contour with a parent and no childs
    # The holes will be drawn in red and the parent contour in green
    if (hierarchy[0, cn, 3] != -1) and (hierarchy[0, cn, 2] == -1):
        color = (255, 0, 0)
    else:
        color = (0,255,0)

    #cv2.drawContours(img, contours, cn, color, 2)
    cv2.drawContours(img, [cnt], -1, color, -1)
    # cv.drawContours(	image, contours, contourIdx, color[, thickness[, lineType[, hierarchy[, maxLevel[, offset]]]]]	)

    # Extract and draw the points
    approx = cv2.approxPolyDP(cnt, 0.009 * cv2.arcLength(cnt, True), True)
    n = approx.ravel()
    i = 0
    for j in n:
        if (i % 2 == 0):
            x = n[i]
            y = n[i + 1]

            img = cv2.circle(img, (x, y), 5, (0, 0, 255), -1)
        i = i + 1
    cn += 1


print(hierarchy)
print(hierarchy.shape)

cv2.imshow("input", img)
#cv2.imshow("output",bw)

cv2.waitKey(0)
cv2.destroyAllWindows()