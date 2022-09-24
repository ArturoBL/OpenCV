# Example to crop L/R stereo images from PS4 camera output
import cv2
from imutils.video import FPS



cap = cv2.VideoCapture(0)
# 898 x 200 (240,120,60,30
# 1748 x 408
# 3448 x 808
cap.set(cv2.CAP_PROP_FRAME_WIDTH, 1748)
cap.set(cv2.CAP_PROP_FRAME_HEIGHT, 408)
cap.set(cv2.CAP_PROP_FPS, 120)
fps = FPS().start()
while True:
    _, image = cap.read()
    cv2.imshow("Output", image)
    x = 48
    y = 0
    w = 640
    h = 399
    limg = image[y:y+h, x:x+w]
    x = 688
    rimg = image[y:y + h, x:x + w]
    cv2.imshow("LImg", limg)
    cv2.imshow("RImg", rimg)
    fps.update()
    
    k = cv2.waitKey(1) & 0xFF
    if k == 27:
        break
fps.stop()
print("[INFO] elasped time: {:.2f}".format(fps.elapsed()))
print("[INFO] approx. FPS: {:.2f}".format(fps.fps()))
cv2.destroyAllWindows()
cap.release()
