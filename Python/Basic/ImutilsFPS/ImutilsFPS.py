
from ast import While
from imutils.video import VideoStream
from imutils.video import FPS
import imutils
import cv2


print("[INFO] sampling THREADED frames from webcam...")
vs = VideoStream(src=0).start()
fps = FPS().start()

while True:
    frame = vs.read()
    fps.update()
        
    #cv2.putText(frame, "[INFO] approx. FPS: {:.2f}".format(fps.fps()), (20, 70), cv2.FONT_HERSHEY_PLAIN, 3, (0, 255, 0), 3)
    cv2.imshow("Frame", frame)
    k = cv2.waitKey(1) & 0xFF
    if k == 27:
        break        

# stop the timer and display FPS information
fps.stop()
print("[INFO] elasped time: {:.2f}".format(fps.elapsed()))
print("[INFO] approx. FPS: {:.2f}".format(fps.fps()))

# do a bit of cleanup
cv2.destroyAllWindows()
vs.stop()