import cv2
import time

cap = cv2.VideoCapture(0)
# cap.set(cv2.CAP_PROP_FRAME_WIDTH, 1748)
# cap.set(cv2.CAP_PROP_FRAME_HEIGHT, 408)
# cap.set(cv2.CAP_PROP_FPS, 120)
cap.set(cv2.CAP_PROP_FRAME_WIDTH, 898)
cap.set(cv2.CAP_PROP_FRAME_HEIGHT, 200)
cap.set(cv2.CAP_PROP_FPS, 120)
pTime = 0

start = time.time()
frames = 0
fps = 0
while True:
    _, image = cap.read()
    frames = frames + 1    
    #cv2.putText(image, f'FPS: {int(fps)}', (20, 70), cv2.FONT_HERSHEY_PLAIN, 3, (0, 255, 0), 3)    
    end = time.time()
    fps = frames /(end - start)
    cv2.putText(image, f'FPS: {int(fps)}', (20, 70), cv2.FONT_HERSHEY_PLAIN, 3, (0, 255, 0), 3)    
    cv2.imshow("Output", image)
    
    k = cv2.waitKey(1) & 0xFF
    if k == 27:
        break

seconds = end - start
print ("Time taken : {0} seconds".format(seconds))


cv2.destroyAllWindows()
cap.release()
