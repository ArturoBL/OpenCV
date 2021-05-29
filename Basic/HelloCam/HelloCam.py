import cv2
from imutils.video import FPS

cap = cv2.VideoCapture(0)
cap.set(cv2.CAP_PROP_FRAME_WIDTH, 640)
cap.set(cv2.CAP_PROP_FRAME_HEIGHT, 480)
cap.set(cv2.CAP_PROP_FPS, 70)
fps = FPS().start()
while True:
    _, image = cap.read()
    cv2.imshow("Output", image)
    fps.update()
    k = cv2.waitKey(1) & 0xFF
    if k == 27:
        break
fps.stop()
print("[INFO] elasped time: {:.2f}".format(fps.elapsed()))
print("[INFO] approx. FPS: {:.2f}".format(fps.fps()))
cv2.destroyAllWindows()
cap.release()
