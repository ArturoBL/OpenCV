import cv2

cap = cv2.VideoCapture(0,cv2.CAP_DSHOW)     # Device Initialization with directshow
cap.set(cv2.CAP_PROP_FRAME_WIDTH, 640)
cap.set(cv2.CAP_PROP_FRAME_HEIGHT, 480)
cap.set(cv2.CAP_PROP_FPS, 60)

while True:
    _, image = cap.read()
    cv2.imshow("Output", image)

    #Exit when ESC key pressed
    k = cv2.waitKey(1) & 0xFF
    if k == 27:     
        break

cv2.destroyAllWindows()
cap.release()