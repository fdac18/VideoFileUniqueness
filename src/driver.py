########################################
# Project: Video File Uniqueness
# Professor: Dr. Audris Mockus
########################################

import argparse
import pandas as pd
import cv2 
from quantzxn import *
from geom import *
from storage import *
from read_frame import *
from write_frame import *
#from Kmeans import CLUSTER
from Kmeans import *
import glob

## Parse the arguments.
parse = argparse.ArgumentParser()
parse.add_argument("data_path", help="Absolute path of directory containing the raw data.")
parsedargs = parse.parse_args()

## Check for errors in the command-line arguments.
path = parsedargs.data_path

## Generate list of strings of video file names using glob or subprocess.
data = glob.glob(path + "/*.avi")

## Instantiate the database.
fname = file_creation()
dbref = connectDB(fname)

## Go through videos, go through frames, store the data.
# for each video:
allcands = []
backtrack = []
nth_frame = 20
for i in range(len(data)):
	# Add video to DB.
	vidno = addDB_Vid(dbref, data[i])
	
	# Go through frames.
	vidcap = cv2.VideoCapture(data[i])
	success,frm = vidcap.read()
	count = 0
	success = True

	while success:
		success,image = vidcap.read()
		print('read a new frame:',success)
		if count % nth_frame == 0 :
			(rs,gs,bs) = quantize_image(frm, 5)
			(res, ims) = top5geo(frm)
			fidno = addDB_Frame(dbref, vidno, str(0), rs, gs, bs, res, ims)	
			#print(get_Frames(dbref, vidno))
			#print(get_Vid_ID(dbref, "/home/dbarry/Video"))	
			
			print('success')
		count+=1

	summary = get_Frames(dbref, vidno)
	framatrix = []
	for i in range(len(summary)):
		framatrix.append([])
		for j in range(3,len(summary[i])):
			framatrix[len(framatrix)-1].append(summary[i][j])
	#print(summary)
	#print(framatrix)
	candidates = CLUSTER(framatrix)
	backtrack.append(candidates)
	#print(candidates)
	candmatrix = []
	for item in candidates:
		candmatrix.append([])
		dat = summary[item]
		for j in range(3,len(dat)):
			candmatrix[len(candmatrix)-1].append(dat[j])
	allcands.append(candmatrix)

#print(candmatrix)
print(allcands)
print("\n")
results=PicVframes(allcands)
print(results)
print(backtrack)

for i in range(len(results)):
	print("The thumbnail for video " + str(data[i]) + " is frame " + str(backtrack[i][results[i]]) + " saved in " + str(data[i]) + "_thumbnail.jpg\n")
	write_frame(data[i], backtrack[i][results[i]])


# for each video:
#	get each frame's data from database
#	do PCA and retain first two PC's
#	do clustering and find the most central point to the largest cluster - this will be that video's representative frame
#	keep track of this frame's id

# for each of the videos' special frame...

