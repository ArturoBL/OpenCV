import triangle
import matplotlib.pyplot as plt
import cv2



image = cv2.imread('../../../../Media/contourrect.png')
gray = cv2.cvtColor(image, cv2.COLOR_BGR2GRAY)
ret, thresh = cv2.threshold(gray, 150, 255, cv2.THRESH_BINARY)
contours, hierarchy = cv2.findContours(thresh, cv2.RETR_TREE, cv2.CHAIN_APPROX_NONE)

c = max(contours, key=cv2.contourArea)
index = contours.index(c)
approx = cv2.approxPolyDP(c, 0.001 * cv2.arcLength(c, True), True)
ctm = approx.reshape(-1, 2)
for (x, y) in ctm:
    cv2.circle(image, (x, y), 1, (0, 0, 255), 3)

print("Contour")
print(ctm)

#find holes
holes = list()
for i, h in enumerate(hierarchy[0]):
    if h[3] == index:
        print(i, h)
        ac = cv2.approxPolyDP(contours[i], 0.001 * cv2.arcLength(contours[i], True), True)
        hole = ac.reshape(-1, 2)
        for (x, y) in hole:
            cv2.circle(image, (x, y), 1, (0, 255, 0), 3)
        holes.append(hole)

print("Holes")
print(len(holes))
print(holes)




# Polígono exterior
outer = [[0, 0], [5, 0], [5, 5], [0, 5]]
# Hoyo interior (en sentido horario)
hole = [[2, 2], [3, 2], [3, 3], [2, 3]]

# Construcción de estructura de entrada
vertices = outer + hole
print("Vertices")
print(vertices)
segments = [[i, (i + 1) % len(outer)] for i in range(len(outer))] + \
           [[i + len(outer), ((i + 1) % len(hole)) + len(outer)] for i in range(len(hole))]

print("Segments")
print(segments)

A = {
    'vertices': vertices,
    'segments': segments,
    'holes': [[2.5, 2.5]]  # Un punto dentro del hoyo
}

# Triangulación
B = triangle.triangulate(A, 'p')  # 'p' = PSLG (planar straight line graph)

#print(B)

# Visualización
triangle.compare(plt, A, B)

#plt.show()


cv2.imshow('image', image)
cv2.waitKey(0)
cv2.destroyAllWindows()