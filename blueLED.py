import cv2
import numpy as np


'''
Tunning Parameters
Increasing sensitivity decreases sensivity
Blur Size for lower the fluctuation
'''
SENSITIVITY_VALUE = 63
BLUR_SIZE = 20

def masking(frame):
	'''
	Maksing Blue Color from Background
	Input: Camera Input BGR format
	Output: Blue masked image
	'''
	# Changing image into HSV format for proper segmentation
	hsv = cv2.cvtColor(frame, cv2.COLOR_BGR2HSV)

	# Defining Range for blue color
	lower_red = np.array([110,50,50])
	upper_red = np.array([130,255,255])

	# Creating & applying mask using bitwise operation 
	mask = cv2.inRange(hsv, lower_red, upper_red)
	res = cv2.bitwise_and(frame,frame, mask= mask)
	return res

def detectMotion(thresholdImage,cameraFeed):
	'''
	This function is used for detecting motion in defined ROI
	Input: Binary Image
	Output: Boolean Format (T/F)
	'''
	motionDetected = False
	# temp = thresholdImage.copy()
	_, contours, hierarchy = cv2.findContours(thresholdImage,cv2.RETR_EXTERNAL,cv2.CHAIN_APPROX_SIMPLE)
	# print cv.contours
	if(len(contours)>0):
		motionDetected = True
	else: motionDetected = False
	return motionDetected

def frameDiff(frame1, frame2):
	'''
	Finding difference between two images
	Input: Two Mat format image
	Ouput: Boolean Format (T/F)
	'''
	grayImage1 = cv2.cvtColor(frame1,cv2.COLOR_BGR2GRAY)
	grayImage2 = cv2.cvtColor(frame2,cv2.COLOR_BGR2GRAY)
	differenceImage = cv2.absdiff(grayImage1,grayImage2)
	_,thresholdImage = cv2.threshold(differenceImage,SENSITIVITY_VALUE,255,cv2.THRESH_BINARY)
	thresholdImage = cv2.blur(thresholdImage,(BLUR_SIZE,BLUR_SIZE))
	_,thresholdImage = cv2.threshold(thresholdImage,SENSITIVITY_VALUE,255,cv2.THRESH_BINARY)
	cv2.imshow('Camera2',thresholdImage)
	motionDetected = detectMotion(thresholdImage,frame1)
	return motionDetected

if __name__ == "__main__":
	count_ = 0
	_list = []
	capture = cv2.VideoCapture('videoname')#'http://192.168.43.1:8080/video')
	while True:
		# print type(capture)
		frame1_ = masking(cv2.UMat(capture.read()[1]))
		frame2_ = masking(cv2.UMat(capture.read()[1]))
		
		# For the program output external coding arena :)
		if frameDiff(frame1_, frame2_):
			# print 'Motion Detected : {}'.format(count_)
			# count_ += 1
			_list.append(1)
		else:
			_lis.append(0)

		# Checking Ouput of masked image (for debugging purposes)
		cv2.imshow('Camera',frame1_)
		if cv2.waitKey(1) & 0xFF == ord('q'):
			capture.release()
			cv2.destroyAllWindows()
			print _list
			break
		
		
