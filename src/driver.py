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
from soi import *
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
for i in range(len(data)):
	# Add video to DB.
	vidno = addDB_Vid(dbref, data[i])
	frm = read_frame_from_file(data[i])
	cv2.imwrite("juggle.jpg",frm)
#    for each frame:
#       collect color data
	(rs,gs,bs) = quantize_image(frm, 5)
	#print("RGB Values", rs, gs, bs)
	(res, ims) = top5geo(frm)
	#print("Geometric Data", res, ims)
#	collect geometric data
#	store data in database
	fidno = addDB_Frame(dbref, vidno, str(0), rs, gs, bs, res, ims)	
	get_Frames(dbref, fidno)
	get_Vid_ID(dbref, "/home/dbarry/link.avi")	

# for each video:
#	get each frame's data from database
#	do PCA and retain first two PC's
#	do clustering and find the most central point to the largest cluster - this will be that video's representative frame
#	keep track of this frame's id

# for each of the videos' special frame...

