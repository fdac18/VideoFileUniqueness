import cv2
import numpy as np

## Test the geometry extraction function.
#top5geo(cv2.imread('home.png',0))

def top5geo(img):

	#outimg = img #np.zeros((1,1))

	print(np.shape(img))

	#for i in range(len(img)):
	#	for j in range(len(img[0])):
	#		img[i][j] /= 255.0
	
	img = np.float32(img)/255.0
	outimg = img

	out = cv2.dft(img, outimg, cv2.DFT_COMPLEX_OUTPUT, 0)

	#print(out)

	max = 0
	for i in range(len(out)):
		for j in range(len(out[0])):
			outimg[i][j] = 255.0*np.sqrt(out[i][j][0]**2 + out[i][j][1]**2)
			if outimg[i][j] > max:
				max = outimg[i][j]

	# Scale -- helps with visibility.
	for i in range(len(out)):
		for j in range(len(out[0])):
			outimg[i][j] *= 255.0/max
			#outimg[i][j] = int(outimg[i][j])

	# Find the largest five values.
	index_i = [0, 0, 0, 0, 0]
	index_j = [0, 0, 0, 0, 0]
	value = [0, 0, 0, 0, 0]
	for i in range(len(out)):
		for j in range(len(out[0])):
			m = outimg[i][j]
			for k in range(len(index_i)):
				if m > value[k]:
					#print("Found: " + str(i) + " " + str(j))
					value[k] = m
					index_i[k] = i
					index_j[k] = j
					break
	
	print(index_i)
	print(index_j)

	#print(outimg)

	#cv2.imshow('image',outimg)
	#cv2.waitKey(0)
	#cv2.destroyAllWindows()

	return
