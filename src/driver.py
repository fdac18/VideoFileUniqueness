########################################
# Project: Video File Uniqueness
# Professor: Dr. Audris Mockus
########################################

import argparse
import pandas as pd
from quantzxn import *
from geom import *
from storage import *
import glob

## Parse the arguments.
parse = argparse.ArgumentParser()
parse.add_argument("data_path", help="Absolute path of directory containing the raw data.")
parsedargs = parse.parse_args()

## Check for errors in the command-line arguments.
path = parsedargs.data_path

## Generate list of strings of video file names using glob or subprocess.
data = glob.glob(path + "/*.avi")
print(data)


## Go through videos, go through frames, store the data.
# for each video:
#    for each frame:
#       collect color data
#	rgbs = quantize_image('home.png', 5)
#	print("RGB Values", rgbs)
#	collect geometric data
#	store data in database

# for each video:
#	get each frame's data from database
#	do PCA and retain first two PC's
#	do clustering and find the most central point to the largest cluster - this will be that video's representative frame
#	keep track of this frame's id

# for each of the videos' special frame...

