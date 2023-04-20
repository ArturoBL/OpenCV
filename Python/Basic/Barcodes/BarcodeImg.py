import cv2
import numpy as np
from pyzbar.pyzbar import decode

img = cv2.imread('../../../Media/Barcodes.jpg')
n = 0
for barcode in decode(img):
    print(f"codigo {n}")
    print(f"Info: {barcode.type}")
    print(f"Info: {barcode.data}")
    
    n += 1
    pts = np.array([barcode.polygon],np.int32)
    pts = pts.reshape((-1,1,2))
    cv2.polylines(img,[pts],True,(0,0,255),2)
    


cv2.imshow('Result',img)
cv2.waitKey(0)
cv2.destroyAllWindows()