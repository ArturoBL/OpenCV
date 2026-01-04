import numpy as np
import cv2
from matplotlib import pyplot as plt

filename = '..\..\..\Media\distort.jpg'
img = cv2.imread(filename, cv2.IMREAD_GRAYSCALE) # `<opencv_root>/samples/data/blox.jpg`

# Initiate FAST object with default values
fast = cv2.FastFeatureDetector_create()

# find and draw the keypoints
kp = fast.detect(img,None)
img2 = cv2.drawKeypoints(img, kp, None, color=(255,0,0))

# Print all default params
print( "Threshold: {}".format(fast.getThreshold()) )
print( "nonmaxSuppression:{}".format(fast.getNonmaxSuppression()) )
print( "neighborhood: {}".format(fast.getType()) )
print( "Total Keypoints with nonmaxSuppression: {}".format(len(kp)) )

# Disable nonmaxSuppression
fast.setNonmaxSuppression(0)
kp = fast.detect(img, None)

print( "Total Keypoints without nonmaxSuppression: {}".format(len(kp)) )

img3 = cv2.drawKeypoints(img, kp, None, color=(255,0,0))

cv2.imshow('fast true',img2)
cv2.imshow('fast false',img3)
if cv2.waitKey(0) & 0xff == 27:
    cv2.destroyAllWindows()