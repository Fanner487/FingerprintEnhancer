import cv2
import numpy as np

# The second parameter loads the image in as GREYSCALE without doing all that codey stuff
image = cv2.imread("Fingerprint.jpg", 0)
original = image

# image = cv2.cvtColor(image, cv2.COLOR_BGR2GRAY)
size = np.size(image)
skeleton = np.zeros(image.shape, np.uint8)


kernel = np.ones((5,5),np.float32)/25

blurGaus = cv2.GaussianBlur(image,(5,5),0)

# TESTING: does de-noising, loses some data
#den = cv2.fastNlMeansDenoising(blurgaus,None,10,7,21)
#dstden = cv2.filter2D(den,-1,kernel)
#thden = cv2.adaptiveThreshold(dstden,255,cv2.ADAPTIVE_THRESH_GAUSSIAN_C,cv2.THRESH_BINARY,15,5)



distGaus = cv2.filter2D(blurGaus,-1,kernel)

image = cv2.adaptiveThreshold(distGaus, maxValue = 255, adaptiveMethod = cv2.ADAPTIVE_THRESH_GAUSSIAN_C, 
	thresholdType = cv2.THRESH_BINARY, blockSize = 15, C = 5)

# algorithm eroded and dilated the white space in between each line(?) of the fingerprint
# invert the image to make it work with the print
image = cv2.bitwise_not(image)

# 3,3 works the best apparently
element = cv2.getStructuringElement(cv2.MORPH_CROSS, (3, 3))

done = False

while( not done):

	# this does magical things
	eroded = cv2.erode(image, element)
	temp = cv2.dilate(eroded, element)
	
	#eroded = cv2.dilate(image, element)
	#temp = cv2.erode(eroded, element)
	
	
	temp = cv2.subtract(image, temp)
	skeleton = cv2.bitwise_or(skeleton, temp)
	image = eroded.copy()

	zeros = size - cv2.countNonZero(image)

	if zeros == size:

		done = True

# inverts the colour
skeleton_inverted = cv2.bitwise_not(skeleton)
cv2.imshow("original", original)
cv2.imshow("skeleton", skeleton_inverted)

cv2.waitKey(0)
cv2.destroyAllWindows()