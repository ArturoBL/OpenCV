import cv2
import time

cap = cv2.VideoCapture(0, cv2.CAP_DSHOW)

cap.set(cv2.CAP_PROP_FRAME_WIDTH,320)
cap.set(cv2.CAP_PROP_FRAME_HEIGHT,240)
cap.set(cv2.CAP_PROP_FPS, 150)

(major_ver, minor_ver, subminor_ver) = (cv2.__version__).split('.')
print(major_ver)
fps = cap.get(cv2.CAP_PROP_FPS)

print("Frames per second using video.get(cv2.CAP_PROP_FPS) : {0}".format(fps))
num_frames = 240
print("Capturing {0} frames".format(num_frames))
start = time.time()
for i in range(0, num_frames):
    ret, frame = cap.read()
end = time.time()

seconds = end - start
print ("Time taken : {0} seconds".format(seconds))
fps  = num_frames / seconds
print("Estimated frames per second : {0}".format(fps))
cap.release()