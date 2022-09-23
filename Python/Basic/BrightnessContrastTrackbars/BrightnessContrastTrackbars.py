# Apply Brightness/Contrast to a Image using trackbar controls

import cv2 as cv

# dummy function used to create the trackbars


def empty(a):
    pass

# Linear transformation function for domain change


def transli(pmin, pmax, pmip, pmap):
    a = (pmip-pmap)/(pmin-pmax)
    b = (pmin*pmap - pmip*pmax) / (pmin-pmax)
    return a, b


img = cv.imread('../../../Media/lena.jpg')

# Create the trackbars window
cv.namedWindow("Trackbars")
cv.resizeWindow("Trackbars", 640, 80)
cv.createTrackbar("Brightness", "Trackbars", 30, 100, empty)
cv.createTrackbar("Contrast", "Trackbars", 0, 100, empty)

# Calc the domain change vars
abr, bbr = transli(0, 100, 0, 3)


while True:
    # Get the trackbars values
    tbr = cv.getTrackbarPos("Brightness", "Trackbars")
    rct = cv.getTrackbarPos("Contrast", "Trackbars")

    # change the brightness value, the contrast doesn't need to be changed
    br = tbr * abr + bbr

    # Apply the values
    brimage = cv.convertScaleAbs(img, alpha=br, beta=rct)

    # show the or
    cv.imshow("Original", img)
    cv.imshow("Brightness/Contrast", brimage)
    k = cv.waitKey(1) & 0xFF
    if k == 27:
        break


cv.destroyAllWindows()
