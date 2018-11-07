########################################
# Project: Video File Uniqueness
# Professor: Dr. Audris Mockus
########################################

import argparse
import pandas as pd
import glob

## Parse the arguments.
parse = argparse.ArgumentParser()
parse.add_argument("data_path", help="Absolute path of directory containing the raw data.")
parsedargs = parse.parse_args()

## Check for errors in the command-line arguments.
path = parsedargs.data_path

## Generate list of strings of video file names using glob or subprocess. #ColeF

## Read-in the data structure template.
template = pd.read_csv("template.csv")



## Use glob to generate list of all video files in the specified path.
