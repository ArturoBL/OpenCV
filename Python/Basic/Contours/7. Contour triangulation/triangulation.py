import triangle
import matplotlib.pyplot as plt
import cv2

# Read image

#image = cv2.imread('../../../../Media/contourrect.png')
#image = cv2.imread('../../../../Media/asimetric.png')
image = cv2.imread('../../../../Media/10002EM.png')

image = (255-image)    #Invert when black background
gray = cv2.cvtColor(image, cv2.COLOR_BGR2GRAY)
ret, thresh = cv2.threshold(gray, 150, 255, cv2.THRESH_BINARY)

# Find contours
contours, hierarchy = cv2.findContours(thresh, cv2.RETR_TREE, cv2.CHAIN_APPROX_NONE)

c = max(contours, key=cv2.contourArea)  # Max area contour
mxa = cv2.contourArea(c)
index = contours.index(c)

#epsilon=0.0001      # Lower value = more accurate, more vertices
epsilon=0.0008      # Lower value = more accurate, more vertices
#Reduce number of vertices
approx = cv2.approxPolyDP(c, epsilon * cv2.arcLength(c, True), True)
ctm = approx.reshape(-1, 2)
cxy = [[x, y] for x, y in ctm]  # Convert array to list
seg = [[i, (i + 1) % len(cxy)] for i in range(len(cxy))]    # Create segments


holes = list()  # List of hole vertices
holesct = list()    # List of hole centroids
segh = list()
vertx = cxy
#find child contours
for i, h in enumerate(hierarchy[0]):
    
    if h[3] == index:
        cha = cv2.contourArea(contours[i])
        if cha/mxa < 0.01:
            continue    # Skip small contours
        cp = cv2.approxPolyDP(contours[i], epsilon * cv2.arcLength(contours[i], True), True)
        cp = cp.reshape(-1, 2)
        
        hxy = [[x, y] for x, y in cp]   # Convert array to list        
                
        segh = [[i+len(vertx), (i + 1) % len(hxy) + len(vertx)] for i in range(len(hxy))]
        vertx = vertx + hxy
        
        holes = holes + hxy
        
        #segh = [[i+len(cxy), (i + 1) % len(hxy) + len(cxy)] for i in range(len(hxy))]
        seg = seg + segh
        M = cv2.moments(contours[i])
        hcx = M["m10"] / M["m00"]
        hcy = M['m01'] / M['m00']
        cv2.circle(image, (int(hcx), int(hcy)), 3, (0, 0, 255), -1)
        holesct = holesct + [[int(hcx), int(hcy)]]    # Add hole centroid to list                   

for x, y in vertx:
    cv2.circle(image, (x, y), 3, (0, 255, 0), -1)

#print("vertx",vertx)
#print("seg",seg)
#print("holesct",holesct)


A = {
    'vertices': vertx,
    'segments': seg,
    'holes': holesct
}
#B = triangle.triangulate(A)  # Delaunay triangulation
B = triangle.triangulate(A, 'p')  # 'p' = PSLG (planar straight line graph)    
#B = triangle.triangulate(A, 'pc')  # 'pc' = PSLG with constrained Delaunay
#B = triangle.triangulate(A, 'pq10')  # 'pq10' = PSLG with quality = 10
#B = triangle.triangulate(A, 'pq0D')  # 'pq0D' = PSLG with quality = 0 and Delaunay

triangle.compare(plt, A, B)

cv2.imshow('image', image)
plt.gca().invert_yaxis()
plt.show()


cv2.waitKey(0)
cv2.destroyAllWindows()
