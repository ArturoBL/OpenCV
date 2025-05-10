import cv2
import numpy as np

#Load image
image = cv2.imread('../../../../Media/10002EM.png')
#image = (255-image)    #Invert when black background

#preprocess
inv = (255-image)
gray = cv2.cvtColor(inv, cv2.COLOR_BGR2GRAY)

ret, thresh = cv2.threshold(gray, 150, 255, cv2.THRESH_BINARY)

#find contours with RETR_TREE hierarchy mode
contours, hierarchy = cv2.findContours(thresh, cv2.RETR_TREE, cv2.CHAIN_APPROX_NONE)

#Find the biggest contour area
mxi = 0     
mxa = cv2.contourArea(contours[0])     
for i, contour in enumerate(contours):    
    area = cv2.contourArea(contour)
    if area > mxa:
        mxi = i         #index
        mxa = area      #area

print("Biggest area: ", mxa)

#Find the child contours correspondig to holes in the biggest contour
childs = list()
ha = 0      #holes area
for i, h in enumerate(hierarchy[0]):    
    if h[3] == mxi:     #if parent is the biggest contour
        cha = cv2.contourArea(contours[i])
        
        if cha/mxa < 0.01:  #ignore small holes < 1%
            print(f"Child area: {cha} rejected")
            continue
        
        ha += cha
        print("Child area: ", cha)
        childs.append(i)        

print("Number of holes: ", len(childs))        
print(childs)
print("Total holes area: ", ha)
print("Contour solid area: ", mxa - ha)

height, width, _ = image.shape
mask = np.zeros((height, width, 3), np.uint8)
cv2.fillPoly(mask, pts =[contours[mxi]], color=(0,0,255))   #Contour in red
cv2.fillPoly(mask, pts =[contours[i] for i in childs], color=(0,0,0))   #Holes in black

#Mark the biggest contour in red
segmentation = cv2.bitwise_or(image,mask)

cv2.imshow('image', image)
cv2.imshow('Mask', mask)
cv2.imshow('Contour Segmentation', segmentation)
cv2.waitKey(0)
cv2.destroyAllWindows()