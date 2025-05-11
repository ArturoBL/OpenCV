import cv2

host = '192.169.x.x'
user = 'myuser'
password = 'mypassword'
url = f"rtsp://{user}:{password}@{host}"
cap =cv2.VideoCapture(url)

while True:
    _, image = cap.read()
    cv2.imshow("Output", image)
    k = cv2.waitKey(1) & 0xFF
    if k == 27:
        break

cv2.destroyAllWindows()
cap.release()