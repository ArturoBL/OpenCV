# Basado en el código de OMES: https://github.com/GabySol/OmesTutorials/tree/master/Detecci%C3%B3n%20de%20Rostros
import cv2
import time

faceClassif = cv2.CascadeClassifier('../../../../Media/haarcascade_frontalface_default.xml')

# cap = cv2.VideoCapture(2,cv2.CAP_DSHOW)
# cap.set(cv2.CAP_PROP_FRAME_WIDTH, 320)
# cap.set(cv2.CAP_PROP_FRAME_HEIGHT, 240)
# cap.set(cv2.CAP_PROP_FPS, 60)
cap = cv2.VideoCapture(0)
# cap.set(cv2.CAP_PROP_FRAME_WIDTH, 1748)
# cap.set(cv2.CAP_PROP_FRAME_HEIGHT, 408)
# cap.set(cv2.CAP_PROP_FPS, 60)
cap.set(cv2.CAP_PROP_FRAME_WIDTH, 898)
cap.set(cv2.CAP_PROP_FRAME_HEIGHT, 2000)
cap.set(cv2.CAP_PROP_FPS, 120)

start = time.time()
frames = 0
fps = 0
while True:
    _, image = cap.read()
    gray = cv2.cvtColor(image, cv2.COLOR_BGR2GRAY)
    faces = faceClassif.detectMultiScale(gray,
	scaleFactor=1.1,
	minNeighbors=5,
	minSize=(30,30),
	maxSize=(200,200))
    for (x,y,w,h) in faces:
	    cv2.rectangle(image,(x,y),(x+w,y+h),(0,255,0),2)    
    
    frames = frames + 1 
    end = time.time()
    fps = frames /(end - start)
    cv2.putText(image, f'FPS: {int(fps)}', (20, 70), cv2.FONT_HERSHEY_PLAIN, 3, (0, 255, 0), 3)    
    cv2.imshow("Output", image)
    k = cv2.waitKey(1) & 0xFF
    if k == 27:
        break

cv2.destroyAllWindows()
cap.release()
