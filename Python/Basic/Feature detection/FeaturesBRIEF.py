import numpy as np
import cv2
from matplotlib import pyplot as plt

filename = '..\..\..\Media\distort.jpg'
img = cv2.imread(filename, cv2.IMREAD_GRAYSCALE)

# Initiate FAST detector
star = cv2.xfeatures2d.StarDetector_create()

# Initiate BRIEF extractor
# Requieres opencv-contrib-python package (nonfree  module)
brief = cv2.xfeatures2d.BriefDescriptorExtractor_create()

# find the keypoints with STAR
kp = star.detect(img,None)

# compute the descriptors with BRIEF
kp, des = brief.compute(img, kp)

print( brief.descriptorSize() )
print( des.shape )