import cv2
import time
from collections import deque

cap = cv2.VideoCapture(2, cv2.CAP_V4L2)
cap.set(cv2.CAP_PROP_FRAME_WIDTH, 320)
cap.set(cv2.CAP_PROP_FRAME_HEIGHT, 240)
cap.set(cv2.CAP_PROP_FPS, 187)
cap.set(cv2.CAP_PROP_BUFFERSIZE, 1)

# --- Config FPS ---
fps_window = 30                 # frames para suavizar
timestamps = deque(maxlen=fps_window)

while True:
    ret, frame = cap.read()
    if not ret:
        break

    # === Tu procesamiento aquí ===
    gray = cv2.cvtColor(frame, cv2.COLOR_BGR2GRAY)

    # === Medición FPS real ===
    now = time.perf_counter()
    timestamps.append(now)

    if len(timestamps) >= 2:
        fps = (len(timestamps) - 1) / (timestamps[-1] - timestamps[0])
    else:
        fps = 0.0

    # === HUD ===
    cv2.putText(
        gray,
        f"FPS: {fps:5.1f}",
        (20, 40),
        cv2.FONT_HERSHEY_SIMPLEX,
        1.0,
        (255, 255, 255),
        2,
        cv2.LINE_AA
    )

    cv2.imshow("FPS HUD", gray)

    if cv2.waitKey(1) & 0xFF == 27:
        break

cap.release()
cv2.destroyAllWindows()
