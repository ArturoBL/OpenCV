import cv2
import numpy as np

cap = cv2.VideoCapture(0)
#cap = cv2.VideoCapture(1,cv2.CAP_DSHOW)
#cap.set(cv2.CAP_PROP_FRAME_WIDTH, 320)
#cap.set(cv2.CAP_PROP_FRAME_HEIGHT, 240)
#cap.set(cv2.CAP_PROP_FPS, 70)

net = cv2.dnn.readNetFromCaffe("../../../../Media/deploy.prototxt.txt", "../../../../Media/res10_300x300_ssd_iter_140000.caffemodel")
net.setPreferableBackend(cv2.dnn.DNN_BACKEND_CUDA)
net.setPreferableTarget(cv2.dnn.DNN_TARGET_CUDA)
# Selecciona la GPU (por ejemplo, la 1)
cv2.cuda.setDevice(1)

while True:
    _, image = cap.read()
    (h, w) = image.shape[:2]
    blob = cv2.dnn.blobFromImage(cv2.resize(image, (300, 300)), 1.0,
                                 (300, 300), (104.0, 177.0, 123.0))
    net.setInput(blob)
    detections = net.forward()

    # loop over the detections
    for i in range(0, detections.shape[2]):
        confidence = detections[0, 0, i, 2]

        # filter out weak detections by ensuring the `confidence` is
        # greater than the minimum confidence
        if confidence >= 0.3:
            # compute the (x, y)-coordinates of the bounding box for the
            # object
            box = detections[0, 0, i, 3:7] * np.array([w, h, w, h])
            (startX, startY, endX, endY) = box.astype("int")

            # draw the bounding box of the face along with the associated
            # probability
            text = f"{(confidence * 100):.2f}%"
            y = startY - 10 if startY - 10 > 10 else startY + 10



            cv2.rectangle(image, (startX, startY), (endX, endY),
                          (0, 255, 0), 2)
            cv2.putText(image, text, (startX, y),
                        cv2.FONT_HERSHEY_SIMPLEX, 0.45, (0, 255, 0), 2)

    cv2.imshow("Output", image)

    k = cv2.waitKey(1) & 0xFF
    if k == 27:
        break
cv2.destroyAllWindows()
cap.release()