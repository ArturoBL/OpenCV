#Oritinal repository: https://github.com/xinntao/ESRGAN
#Tutorial: https://www.youtube.com/watch?v=67hqsP7fhvQ&ab_channel=NicholasRenotte

#Models: https://drive.google.com/drive/u/0/folders/17VYV_SoZZesU6mbxz2dMAIccSSlqLecY
#Tutorial's model: RRDB_ESRGAN_x4.pth 

import cv2
import torch
import RRDBNet_arch as arch
import numpy as np

# read the original image
image = cv2.imread('../../../../Media/comic.png',cv2.IMREAD_COLOR)
imgsize = image.shape[:2]

# Upscale with nearest neighbor
newsize = (imgsize[1]*4, imgsize[0]*4)
imgnearest = cv2.resize(image, newsize, interpolation=cv2.INTER_NEAREST)

# Upscale with ESRGAN
model_path = 'RRDB_ESRGAN_x4.pth'  # models/RRDB_ESRGAN_x4.pth OR models/RRDB_PSNR_x4.pth
device = torch.device('cuda')  # if you want to run on CPU, change 'cuda' -> cpu
model = arch.RRDBNet(3, 3, 64, 23, gc=32)
model.load_state_dict(torch.load(model_path), strict=True)
model.eval()
model = model.to(device)

img = image * 1.0 / 255
img = torch.from_numpy(np.transpose(img[:, :, [2, 1, 0]], (2, 0, 1))).float()
img_LR = img.unsqueeze(0)
img_LR = img_LR.to(device)
with torch.no_grad():
    output = model(img_LR).data.squeeze().float().cpu().clamp_(0, 1).numpy()
output = np.transpose(output[[2, 1, 0], :, :], (1, 2, 0))
output = (output * 255.0).round()
cv2.imwrite('output.png', output)
imgout = cv2.imread('output.png')

# Display the images
cv2.imshow('Original',image)
cv2.imshow('Nearest',imgnearest)
cv2.imshow('Upscaled',imgout)
cv2.waitKey(0)
cv2.destroyAllWindows()

