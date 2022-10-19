from imutils.video import VideoStream
import cv2
import time

vs = VideoStream(src=0).start()
start = time.time()
frames = 0
fps = 0

while True:
    frame = vs.read()
    frames = frames + 1
    end = time.time()
    if (end - start) > 1:
        fps = frames /(end - start)
        cv2.putText(frame, f'FPS: {int(fps)}', (20, 70), cv2.FONT_HERSHEY_PLAIN, 3, (0, 255, 0), 3) 
    cv2.imshow("Frame", frame)
    k = cv2.waitKey(1) & 0xFF
    if k == 27:
        break  
vs.stop()
cv2.destroyAllWindows()
