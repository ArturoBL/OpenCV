import cv2
import time

cap = cv2.VideoCapture(2, cv2.CAP_V4L2)
cap.set(cv2.CAP_PROP_FRAME_WIDTH, 320)
cap.set(cv2.CAP_PROP_FRAME_HEIGHT, 240)
cap.set(cv2.CAP_PROP_FPS, 187)

frame_count = 0
start_time = time.perf_counter()
while True:
    _, image = cap.read()
    cv2.imshow("Output", image)
    
    frame_count += 1
    elapsed = time.perf_counter() - start_time
    
    k = cv2.waitKey(1) & 0xFF
    if k == 27:
        break

if elapsed >= 1.0:
        fps = frame_count / elapsed
        print(f"FPS: {fps:.2f}")
        frame_count = 0
        start_time = time.perf_counter()

cv2.destroyAllWindows()
cap.release()
