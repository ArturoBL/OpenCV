import cv2
import time

cap = cv2.VideoCapture(2, cv2.CAP_V4L2)
cap.set(cv2.CAP_PROP_FRAME_WIDTH, 320)
cap.set(cv2.CAP_PROP_FRAME_HEIGHT, 240)
cap.set(cv2.CAP_PROP_FPS, 187)

tick_start = cv2.getTickCount()
frames = 0

while True:
    ret, frame = cap.read()
    if not ret:
        break

    frames += 1

    tick_end = cv2.getTickCount()
    time_sec = (tick_end - tick_start) / cv2.getTickFrequency()

    if frames >= 1000:
        break
    

if time_sec >= 1.0:
    fps = frames / time_sec
    print(f"FPS: {fps:.2f}")
    frames = 0
    tick_start = cv2.getTickCount()