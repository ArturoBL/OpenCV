import cv2

cap = cv2.VideoCapture(0,cv2.CAP_DSHOW)     # Device Initialization with directshow
cap.set(cv2.CAP_PROP_FRAME_WIDTH, 640)
cap.set(cv2.CAP_PROP_FRAME_HEIGHT, 480)
cap.set(cv2.CAP_PROP_FPS, 60)
n = 0

chessboardSize = (9,6)
criteria = (cv2.TERM_CRITERIA_EPS + cv2.TERM_CRITERIA_MAX_ITER, 30, 0.001)

while True:
    _, image = cap.read()
    img2 = image.copy()
    
    gray = cv2.cvtColor(image, cv2.COLOR_BGR2GRAY)

    # Find the chess board corners
    ret, corners = cv2.findChessboardCorners(gray, chessboardSize, None)

    if ret == True:
        corners2 = cv2.cornerSubPix(gray, corners, (11,11), (-1,-1), criteria)
        cv2.drawChessboardCorners(img2, chessboardSize, corners2, ret)
    cv2.imshow("Output", img2) #show image with drawn chessboard to save the original
   
    #Save image when any key is pressed
    k = cv2.waitKey(1) & 0xFF
    if k != 255 and k != 27 and ret==True:  # save only images with detected chessboard
        cv2.imwrite(f"image{n}.jpg", image)
        print(f"image{n}.jpg saved!")
        n += 1
    if k == 27:     #Exit when ESC key pressed
        break

cv2.destroyAllWindows()
cap.release()