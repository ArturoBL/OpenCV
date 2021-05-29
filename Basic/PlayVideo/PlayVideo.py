import cv2

#Abrimos stream de video desde archivo
cap = cv2.VideoCapture('../../Media/video.mp4')

#Ciclo para leer cada frame de video
while(cap.isOpened()):
    #Leemos frame
    ret, frame = cap.read()

    #Si se obtiene frame se muestra en ventana con tìtulo frame
    if ret:
        cv2.imshow('Frame',frame)
    else:
        break
    if cv2.waitKey(1) & 0xFF == 27:
        break

#Liberamos stream
cap.release()
cv2.destroyAllWindows()