import cv2

cap = cv2.VideoCapture(0)
cap.set(cv2.CAP_PROP_FRAME_WIDTH, 640)
cap.set(cv2.CAP_PROP_FRAME_HEIGHT, 480)
cap.set(cv2.CAP_PROP_FPS, 150)

rec = cv2.VideoWriter('video.avi', cv2.VideoWriter_fourcc(*'XVID'),30.0,(640,480))

while True:
    _, image = cap.read()
    cv2.imshow("Output", image)
    rec.write(image)
    k = cv2.waitKey(1) & 0xFF
    if k == 27:
        break
rec.release()
cv2.destroyAllWindows()
cap.release()
