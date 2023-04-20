import cv2
import pickle

cap = cv2.VideoCapture(0,cv2.CAP_DSHOW)     # Device Initialization with directshow
cap.set(cv2.CAP_PROP_FRAME_WIDTH, 640)
cap.set(cv2.CAP_PROP_FRAME_HEIGHT, 480)
cap.set(cv2.CAP_PROP_FPS, 60)
n = 0

chessboardSize = (9,6)
frameSize = (640,480)
criteria = (cv2.TERM_CRITERIA_EPS + cv2.TERM_CRITERIA_MAX_ITER, 30, 0.001)
objp = np.zeros((chessboardSize[0] * chessboardSize[1], 3), np.float32)
objp[:,:2] = np.mgrid[0:chessboardSize[0],0:chessboardSize[1]].T.reshape(-1,2)
size_of_chessboard_squares_mm = 20
objp = objp * size_of_chessboard_squares_mm
objpoints = [] # 3d point in real world space
imgpoints = [] # 2d points in image plane.

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
        objpoints.append(objp)        
        corners2 = cv2.cornerSubPix(gray, corners, (11,11), (-1,-1), criteria)
        imgpoints.append(corners)

        cv2.imwrite(f"image{n}.jpg", image)
        print(f"image{n}.jpg saved!")
        n += 1
    if k == 27:     #Exit when ESC key pressed
        break

if n > 0:
    #Calibration returns camera matrix, distortion coefficients, rotation vector, traslation vector
    ret, cameraMatrix, dist, rvecs, tvecs = cv2.calibrateCamera(objpoints, imgpoints, frameSize, None, None)
    cameraparameters = {
        'Matrix': cameraMatrix,
        'dist': dist,
        'rvecs': rvecs,
        'tvecs': tvecs
    }

    with open('camera_parameters.pkl', 'wb') as cfile:
        pickle.dump(cameraparameters, cfile)
    print("Camera parametes saved to file!") 

    # re-projection error: The closer the re-projection error is to zero, the more accurate the parameters we found are
    mean_error = 0
    for i in range(len(objpoints)):
        imgpoints2, _ = cv2.projectPoints(objpoints[i], rvecs[i], tvecs[i], cameraMatrix, dist)
        error = cv2.norm(imgpoints[i], imgpoints2, cv2.NORM_L2)/len(imgpoints2)
        mean_error += error
    print( "total error: {}".format(mean_error/len(objpoints)) )
else:
    print("No images captured.")    

cv2.destroyAllWindows()
cap.release()