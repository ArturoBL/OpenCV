from imutils.video import VideoStream
import imutils
import numpy as np
import cv2

net = cv2.dnn.readNetFromCaffe("../../../../Media/deploy.prototxt.txt", "../../../../Media/res10_300x300_ssd_iter_140000.caffemodel")

net.setPreferableBackend(cv2.dnn.DNN_BACKEND_CUDA)
net.setPreferableTarget(cv2.dnn.DNN_TARGET_CUDA)

vs = VideoStream(src=0).start()

while True:
    frame = vs.read()
    frame = imutils.resize(frame, width=400)

    (h, w) = frame.shape[:2]
    blob = cv2.dnn.blobFromImage(cv2.resize(frame, (300, 300)), 1.0,
                                 (300, 300), (104.0, 177.0, 123.0))

    net.setInput(blob)
    detections = net.forward()

    for i in range(0, detections.shape[2]):
        confidence = detections[0, 0, i, 2]

        if confidence <  0.5:
            continue

        box = detections[0, 0, i, 3:7] * np.array([w, h, w, h])
        (startX, startY, endX, endY) = box.astype("int")

        face = frame[startY:endY, startX:endX]
        height, width = face.shape[:2]
        lowh = int(height / 15)
        loww = int(width / 15)

        temp = cv2.resize(face, (loww, lowh), interpolation=cv2.INTER_LINEAR)
        pxface = cv2.resize(temp, (width, height), interpolation=cv2.INTER_NEAREST)

        cv2.imshow("pxFace", pxface)

        cv2.imshow("face", face)
        frame[startY:endY, startX:endX] = pxface
        #cv2.rectangle(frame, (startX, startY), (endX, endY),
        #              (0, 0, 255), 2)

    cv2.imshow("Frame", frame)

    key = cv2.waitKey(1) & 0xFF

    # if the `q` key was pressed, break from the loop
    if key == ord("q"):
        break

cv2.destroyAllWindows()
vs.stop()