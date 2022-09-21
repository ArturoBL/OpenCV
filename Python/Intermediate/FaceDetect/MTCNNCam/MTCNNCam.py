#MTCNN for tensorflow (CUDA) face detector
import cv2
from mtcnn.mtcnn import MTCNN
detector = MTCNN()

cap = cv2.VideoCapture(0)

while (True):
    ret, frame = cap.read()
    if ret == True:
        location = detector.detect_faces(frame)
        if len(location) > 0:
            for face in location:
                x, y, width, height = face['box']
                x2, y2 = x + width, y + height
                cv2.rectangle(frame, (x, y), (x2, y2), (0, 0, 255), 4)
        cv2.imshow("Output",frame)
        if cv2.waitKey(1) & 0xFF == ord('q'):
            break
    else:
        break

cap.release()
cv2.destroyAllWindows()