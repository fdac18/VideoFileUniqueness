#!/usr/bin/env
# This file contains functions which can be called to create and modify a database for the video file uniqueness project
# this file when run on its own will create the initial database and tables, and can be referenced by other python files to easily add and remove data from tables
# the contents of this are based on the tutorial at sqlitetutorial.net

import sqlite3
from sqlite3 import Error

def connectDB(fName):
	#this is a basic function which will make the database file 
	# this function must be run at the start of the file and it returns cnnct which is used by other functions to connect to the database file
	try:
		cnnct = sqlite3.connect(fName)
		return cnnct
	except Error as e:
		print(e)
	return None

def make_table(cnnct, create_table_sql):
	try:
		c = cnnct.cursor()
		c.execute(create_table_sql)
	except Error as e:
		print(e)

def addDB_Vid(cnnct, newVidName):
	#this function adds a Video to the database
	#this one will create the video data and also two empty frame objects
	sql = ''' INSERT INTO  videos(name, chosenFrameID)
			  VALUES(?, 0)'''
	curs = cnnct.cursor()
	curs.execute(sql, newVidName)
	# this will return the id of the video
	return curs.lastrowid

def addDB_frame(cnnct, vidID, newName, newRedArr, newGrnArr, newBluArr, newReals, newImags):
	#this should update a targeted frame as we create frames when we make videos all 'added' frames done by other programs is actually a matter of updating them
	# in theory the ID of the frame for a given video should have the id of vid_id * 2 + 0 for average and + 1 for unique
	newFrame = []
	newFrame[0] = newName
	newFrame[1] = vidID
	newFrame = newFrame + newRedArr + newGrnArr + newBluArr + newReals + newImags
	sql = ''' INSERT INTO frames( 
			  	  name, tableID
				  red_val_0, red_val_1, red_val_2, red_val_3, red_val_4,
				  grn_val_0, grn_val_1, grn_val_2, grn_val_3, grn_val_4,
				  blu_val_0, blu_val_1, blu_val_2, blu_val_3, blu_val_4,
				  reals_0, reals_1, reals_2, reals_3, reals_4,
				  imags_0, imags_1, imags_2, imags_3,imags_4) 
			  VALUES(?,?,?,?,?,?,?,?,?,?,?,?,?,?,?,?,?,?,?,?,?,?,?,?,?,?,?)'''
	curs = cnnct.cursor()
	curs.execute(sql, newFrame)
	return curs.lastrowid

def main():
	db = VFU_DB.db
	sql_create_video_table = """ CREATE TABLE IF NOT EXISTS videos (
		id integer PRIMARY KEY,
		name text NOT NULL,
		chosenFrameID integer
		); """

	sql_create_frame_table = """CREATE TABLE IF NOT EXISTS frames (
		id integer PRIMARY KEY,
		vid_id integer NOT NULL,
		name text NOT NULL,
		red_val_0 integer NOT NULL,
		red_val_1 integer NOT NULL,
		red_val_2 integer NOT NULL,
		red_val_3 integer NOT NULL,
		red_val_4 integer NOT NULL,
		grn_val_0 integer NOT NULL,
		grn_val_1 integer NOT NULL,
		grn_val_2 integer NOT NULL,
		grn_val_3 integer NOT NULL,
		grn_val_4 integer NOT NULL,
		blu_val_0 integer NOT NULL,
		blu_val_1 integer NOT NULL,
		blu_val_2 integer NOT NULL,
		blu_val_3 integer NOT NULL,
		blu_val_4 integer NOT NULL,
		reals_0 integer NOT NULL,
		reals_1 integer NOT NULL,
		reals_2 integer NOT NULL,
		reals_3 integer NOT NULL,
		reals_4 integer NOT NULL,
		imags_0 integer NOT NULL,
		imags_1 integer NOT NULL,
		imags_2 integer NOT NULL,
		imags_3 integer NOT NULL,
		imags_4 integer NOT NULL,
		FOREIGN KEY (vid_id) REFERENCES videos (id)
	);"""

	con = connectDB(db)
	if con is not None:
		# make our tables
		make_table(con, sql_create_video_table)
		make_table(con, sql_create_frame_table)
	else:
		print("error encountered no database connection")

# if this file is run on its own it runs main and will create the database file and its tables
if __name__ == '__main__':
	main()
