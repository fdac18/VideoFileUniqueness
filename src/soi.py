import numpy as np
import cv2

def read_frame_from_file(filename):

	cap = cv2.VideoCapture(filename)
	ret, frame = cap.read()
	#gray = cv2.cvtColor(frame, cv2.COLOR_BGR2GRAY)

	return frame
