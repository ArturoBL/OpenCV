import cv2 as cv

# Load images and check if they loaded properly
img1 = cv.imread('../../../../Media/nightsky.png')
img2 = cv.imread('../../../../Media/moon.png')

if img1 is None or img2 is None:
    print("Error loading images. Please make sure both nightsky.png and moon.png exist in the same directory as this script.")
    exit(1)

# Get dimensions of both images
img1_height, img1_width = img1.shape[:2]
img2_height, img2_width = img2.shape[:2]

# Resize moon image to match night sky dimensions
if img2_height != img1_height or img2_width != img1_width:
    print(f"Resizing moon image from {img2.shape} to match night sky dimensions {img1.shape}")
    img2 = cv.resize(img2, (img1_width, img1_height))

img_2_shape = img2.shape

# Get dimensions of both images
img1_height, img1_width = img1.shape[:2]
img2_height, img2_width = img2.shape[:2]

# Create ROI that matches moon image dimensions
roi = img1[0:img2_height, 0:img2_width]

# Convert to grayscale and create mask
img2gray = cv.cvtColor(img2, cv.COLOR_BGR2GRAY)
ret, mask = cv.threshold(img2gray, 10, 255, cv.THRESH_BINARY)
mask_inv = cv.bitwise_not(mask)

# Check mask dimensions
if roi.shape[:2] != mask.shape[:2]:
    print(f"Error: ROI and mask dimensions don't match.")
    print(f"ROI shape: {roi.shape}, Mask shape: {mask.shape}")
    exit(1)

# Print dimensions for debugging
print(f"Image 1 dimensions: {img1.shape}")
print(f"Image 2 dimensions: {img2.shape}")
print(f"ROI dimensions: {roi.shape}")
print(f"Mask dimensions: {mask.shape}")

# Now black-out the area of moon in ROI
img1_bg = cv.bitwise_and(roi,roi,mask = mask_inv)
print(img1.shape, mask.shape)
# Take only region of moon from moon image.
img2_fg = cv.bitwise_and(img2,img2,mask = mask)
# Put moon in ROI and modify the main image
dst = cv.add(img1_bg,img2_fg)
img1[0:img_2_shape[0], 0:img_2_shape[1]] = dst
#Create resizable windows for our display images
cv.namedWindow('img1_bg', cv.WINDOW_NORMAL)
cv.namedWindow('img2_fg', cv.WINDOW_NORMAL)
cv.namedWindow('mask', cv.WINDOW_NORMAL)
cv.namedWindow('maskinv', cv.WINDOW_NORMAL)
cv.namedWindow('res', cv.WINDOW_NORMAL)
cv.imshow('mask',mask)
cv.imshow('maskinv',mask_inv)
cv.imshow('img1_bg',img1_bg)
cv.imshow('img2_fg',img2_fg)
cv.imshow('res',img1)

if cv.waitKey(0) & 0xff == 27:
    cv.destroyAllWindows()