# Contributors: 
# - Oleg Petcov C14399846
# - Cliona Rogers C14396346
# - Eamon Tang C14383761

# Procedure:
# - Apply bilateral filter 
# - Enhance contrast (enhance the lighter areas of the image) 
# - Apply adaptive threshold (get binary mask of fingerprint)
# - Denoise (reduce some noise)
# - Apply Gaussian blur	
# - Invert image colour (so skeletonisation algorithm can work on correct part of fingerprint)
# - Skeletonise
# - Invert image colour (put black fingerprint on white background)
# - Denoise (last steps of cleaning up)
# - Apply bilateral filter


import cv2
import numpy as np
import easygui

# The whole process and sequence of functions called to
# extract and clean up the skeleton of the fingerprint
def process(image):

	# blur and enhance the blackness of the original fingerprint image
	bilateral_filtered = filter_bilateral(image)
	contrast_enhanced = contrast_enhance(bilateral_filtered)
	
	# get binary mask of threshold
	threshold = apply_threshold(contrast_enhanced)
	
	# reduce noise and blur artefects left from denoising 
	denoised = denoise(threshold)
	gaussian_blurred = blur(denoised)

	# invert the binary image so the skeletonisation algorithm works
	# on the lines of the fingerprint, not the spaces between them
	inverted = invert_image(gaussian_blurred)
	
	skeleton = skeletonise(inverted)
	
	# Put the fingerprint back onto a white background
	skeleton_inverted = invert_image(skeleton)

	# Last step touching up and blurring
	skeleton_inverted_denoised = denoise(skeleton_inverted)

	skeleton_inverted_bilateral_filter = filter_bilateral(skeleton_inverted_denoised)


	# # Show images from every step
	# cv2.imshow("bilateral_filtered", bilateral_filtered)
	# cv2.imshow("contrast_enhanced", contrast_enhanced)
	# cv2.imshow("threshold", threshold)
	# cv2.imshow("denoised", denoised)
	# cv2.imshow("gaussian_blurred", gaussian_blurred)
	# cv2.imshow("inverted", inverted)
	# cv2.imshow("skeleton", skeleton)
	# cv2.imshow("skeleton_inverted", skeleton_inverted)
	# cv2.imshow("skeleton_inverted_denoised", skeleton_inverted_denoised)
	# cv2.imshow("skeleton_inverted_bilateral_filter", skeleton_inverted_bilateral_filter)
	# cv2.waitKey(0)
	# cv2.destroyAllWindows()


	return skeleton_inverted_bilateral_filter


# Skeletonisation snippet code:
# Rahman K, Abid, 24/11/2017, Skeletonization using OpenCV-Python, http://opencvpython.blogspot.ie/2012/05/skeletonization-using-opencv-python.html
def skeletonise(image):

	element = cv2.getStructuringElement(cv2.MORPH_CROSS, (3, 3))
	size = np.size(image)

	# A blank image the size of the original image
	skeleton = np.zeros(image.shape, np.uint8)
	done = False
	
	while( not done):
	
		eroded = cv2.erode(image, element)
		dilated = cv2.dilate(eroded, element)
		
		# get the difference from erosion/dilation process from the original image arrays
		subtracted = cv2.subtract(image, dilated)

		# Adds the processed image to skeleton image
		skeleton = cv2.bitwise_or(skeleton, subtracted)

		image = eroded.copy()

		zeros = size - cv2.countNonZero(image)

		# Checks to see if the fingerprint is one pixel wide, I think?
		if zeros == size:

			done = True

	return skeleton


# Inverts a whole greyscale image between black and white
def invert_image(image):

	result = cv2.bitwise_not(image)

	return result


# Using Contrast Limited Adaptive Histogram Equalisation to darken image
def contrast_enhance(image):

	clip_limit = 2.0
	tile_grid_size = (8,8)
	clahe = cv2.createCLAHE(clipLimit=clip_limit, tileGridSize=tile_grid_size)
	
	result = clahe.apply(image)
	
	return result


# Adaptive threshold
def apply_threshold(image):

	max_value = 255
	block_size = 15
	constant = 5

	result = cv2.adaptiveThreshold(image, maxValue = max_value, adaptiveMethod = cv2.ADAPTIVE_THRESH_GAUSSIAN_C, 
		thresholdType = cv2.THRESH_BINARY, blockSize = block_size, C = constant)

	return result

# Using Fast Non-Local Means Deniosing
def denoise(image):

	h = 10
	search_window = 21
	block_size = 7

	result = cv2.fastNlMeansDenoising(image, None, h, block_size, search_window)

	return result


# Using Gaussian Blur
def blur(image):

	block_size = (5,5)

	result = cv2.GaussianBlur(image, block_size, 0)

	return result


# Using a bilateral filter
def filter_bilateral(image):

	diameter = 11
	sigma_colour = 17
	sigma_space = 17

	result = cv2.bilateralFilter(image, diameter, sigma_colour, sigma_space)

	return result


# End methods

file = easygui.fileopenbox()
# The second parameter loads the image in as GREYSCALE without doing all that codey stuff
image = cv2.imread(file, 0)
original = image

processed = process(image)

cv2.imshow("original", original)
cv2.imshow("skeleton", processed)


cv2.imwrite("ShinyFingers.jpg", processed)

cv2.waitKey(0)
cv2.destroyAllWindows()