import dlib
import cv2

def convert_and_trim_bb(image, rect):
	# extract the starting and ending (x, y)-coordinates of the
	# bounding box
	startX = rect.left()
	startY = rect.top()
	endX = rect.right()
	endY = rect.bottom()
	# ensure the bounding box coordinates fall within the spatial
	# dimensions of the image
	startX = max(0, startX)
	startY = max(0, startY)
	endX = min(endX, image.shape[1])
	endY = min(endY, image.shape[0])
	# compute the width and height of the bounding box
	w = endX - startX
	h = endY - startY
	# return our bounding box coordinates
	return (startX, startY, w, h)

detector = dlib.cnn_face_detection_model_v1("../../../../Media/mmod_human_face_detector.dat")
cap = cv2.VideoCapture(0)

while True:
    _, image = cap.read()
    rgb = cv2.cvtColor(image, cv2.COLOR_BGR2RGB)
    results = detector(rgb, 1)
    boxes = [convert_and_trim_bb(image, r.rect) for r in results]
    for (x, y, w, h) in boxes:	
	    cv2.rectangle(image, (x, y), (x + w, y + h), (0, 255, 0), 2)
    cv2.imshow("Output", image)
    
    k = cv2.waitKey(1) & 0xFF
    if k == 27:
        break

cv2.destroyAllWindows()
cap.release()  