import cv2
import numpy as np

# The second parameter loads the image in as GREYSCALE without doing all that codey stuff
image = cv2.imread("fingerprint.jpg", 0)
original = image

# image = cv2.cvtColor(image, cv2.COLOR_BGR2GRAY)
size = np.size(image)
skeleton = np.zeros(image.shape, np.uint8)

clahe = cv2.createCLAHE(clipLimit=2.0, tileGridSize=(8,8))


image = cv2.bilateralFilter(image, 11, 17, 17)

image = clahe.apply(image)

cv2.imshow("clahe", image)


image = cv2.adaptiveThreshold(image, maxValue = 255, adaptiveMethod = cv2.ADAPTIVE_THRESH_GAUSSIAN_C, 
	thresholdType = cv2.THRESH_BINARY, blockSize = 15, C = 5)

cv2.imshow("Threshedimage", image)
	
# algorithm eroded and dilated the white space in between each line(?) of the fingerprint
# invert the image to make it work with the print
denoise = cv2.fastNlMeansDenoising(image,None,10,7,21)
blurGaus = cv2.GaussianBlur(denoise,(5,5),0)

cv2.imshow("blurGaus", blurGaus)

#image = cv2.filter2D(blurGaus,-1,kernel)
image = cv2.bitwise_not(blurGaus)

cv2.imshow("image", image)

# 3,3 works the best apparently
element = cv2.getStructuringElement(cv2.MORPH_CROSS, (3, 3))

done = False

cv2.imshow("image", image)

while( not done):

	# this does magical things
	eroded = cv2.erode(image, element)
	temp = cv2.dilate(eroded, element)
	
	temp = cv2.subtract(image, temp)
	skeleton = cv2.bitwise_or(skeleton, temp)
	image = eroded.copy()

	zeros = size - cv2.countNonZero(image)

	if zeros == size:

		done = True

# inverts the colour

# More denoising to get rid of aliasing
skeleton = cv2.fastNlMeansDenoising(skeleton,None,10,7,21)

'''
thresh = cv2.adaptiveThreshold(skeleton, maxValue = 255, adaptiveMethod = cv2.ADAPTIVE_THRESH_GAUSSIAN_C, 
	thresholdType = cv2.THRESH_BINARY, blockSize = 15, C = 5)
	
	
cv2.imshow("thresh", thresh)
'''

skeleton_inverted = cv2.bitwise_not(skeleton)


cv2.imshow("original", original)
cv2.imshow("skeleton", skeleton_inverted)

cv2.imwrite("ShinyFingeres.jpg", skeleton_inverted)

cv2.waitKey(0)
cv2.destroyAllWindows()