#MediaPipe Cam FaceDetect
import cv2
import mediapipe as mp
mp_face_detection = mp.solutions.face_detection
mp_drawing = mp.solutions.drawing_utils

# For static images:
fdet = mp_face_detection.FaceDetection(min_detection_confidence=0.5)
cap = cv2.VideoCapture(1)
cap.set(cv2.CAP_PROP_FRAME_WIDTH, 640)
cap.set(cv2.CAP_PROP_FRAME_HEIGHT, 480)
cap.set(cv2.CAP_PROP_FPS, 75)
# cap.set(cv2.CAP_PROP_FRAME_WIDTH, 898)
# cap.set(cv2.CAP_PROP_FRAME_HEIGHT, 200)
# cap.set(cv2.CAP_PROP_FPS, 120)

while True:
    _, image = cap.read()
    results = fdet.process(cv2.cvtColor(image, cv2.COLOR_BGR2RGB))
    if results.detections:
        annotated_image = image.copy()
        for detection in results.detections:
            print('Nose tip:')
            print(mp_face_detection.get_key_point(
            detection, mp_face_detection.FaceKeyPoint.NOSE_TIP))
            mp_drawing.draw_detection(image, detection)
    cv2.imshow("Output", image)    
    k = cv2.waitKey(1) & 0xFF
    if k == 27:
        break
