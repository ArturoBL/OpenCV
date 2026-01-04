import cv2
import numpy as np
from matplotlib import pyplot as plt

filename = '..\..\..\Media\distort.jpg'
img = cv2.imread(filename)
gray = cv2.cvtColor(img, cv2.COLOR_BGR2GRAY)

# Create SURF detector object
# hessianThreshold: threshold for the Hessian keypoint detector
# requires opencv-contrib-python package (nonfree module)
surf = cv2.xfeatures2d.SURF_create(hessianThreshold=400)

# Detect keypoints and compute descriptors
keypoints, descriptors = surf.detectAndCompute(gray, None)

print(f"Number of keypoints found: {len(keypoints)}")
print(f"Descriptor shape: {descriptors.shape}")

# Draw keypoints on image
img_keypoints = cv2.drawKeypoints(img, keypoints, None, flags=cv2.DRAW_MATCHES_FLAGS_DRAW_RICH_KEYPOINTS)

# Display the result
cv2.imshow('SURF Keypoints', img_keypoints)
cv2.waitKey(0)
cv2.destroyAllWindows()


# Print keypoint information
for i, kp in enumerate(keypoints[:5]):  # Print first 5 keypoints
    print(f"Keypoint {i}: x={kp.pt[0]:.2f}, y={kp.pt[1]:.2f}, size={kp.size:.2f}, angle={kp.angle:.2f}")