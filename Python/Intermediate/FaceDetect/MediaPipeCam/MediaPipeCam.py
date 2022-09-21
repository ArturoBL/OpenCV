#MediaPipe Cam FaceDetect
import cv2
import mediapipe as mp
mp_face_detection = mp.solutions.face_detection
mp_drawing = mp.solutions.drawing_utils

# For static images:
fdet = mp_face_detection.FaceDetection(min_detection_confidence=0.5)
cap = cv2.VideoCapture(0)
while True:
    _, image = cap.read()
    results = fdet.process(cv2.cvtColor(image, cv2.COLOR_BGR2RGB))
    if results.detections:
        annotated_image = image.copy()
        for detection in results.detections:
            print('Nose tip:')
            print(mp_face_detection.get_key_point(
            detection, mp_face_detection.FaceKeyPoint.NOSE_TIP))
            mp_drawing.draw_detection(annotated_image, detection)
    cv2.imshow("Output", annotated_image)    
    k = cv2.waitKey(1) & 0xFF
    if k == 27:
        break
