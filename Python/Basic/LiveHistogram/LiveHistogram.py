#Code by Arturo Beristain López

import numpy as np
import matplotlib.pyplot as plt
import cv2

capture = cv2.VideoCapture(0,cv2.CAP_DSHOW)

# Initialize plot.
fig, ax = plt.subplots()
plt.ion()
plt.show()

color = ('b', 'g', 'r')

while True:
    (grabbed, frame) = capture.read()

    if not grabbed:
        break
    
    cv2.imshow('RGB', frame)
    ax.cla()        #clear last plot
    for i, col in enumerate(color):
        histr = cv2.calcHist([frame], [i], None, [256], [0, 256])
        
        ax.plot(histr, color=col, alpha=0.5, lw = 2)
        plt.xlim([0, 256])
        plt.title('RGB Histogram')
        ax.set_xlabel('Intensity')
        ax.set_ylabel('Frequency')        
    
    fig.canvas.draw()
    
    if cv2.waitKey(1) & 0xFF == ord('q'):
        break

capture.release()
cv2.destroyAllWindows()