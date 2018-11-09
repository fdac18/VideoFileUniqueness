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
	sql = ''' INSERT INTO  videos(name, avg_frame, best_frame)
			  VALUES(?,?,?)'''
	curs = cnnct.cursor()
	curs.execute(sql, newVid)

	avgFrame = ('Average', curs.lastrowid, 0, 0, 0, 0, 0 )
	uniqueFrame = ('Unique', curs.lastrowid, 0, 0, 0, 0, 0)
	#add frames for average and unique
	addDB_Frame(cnnct, avgFrame) 
	addDB_Frame(cnnct, uniqueFrame)
	# this will return the id of the video
	return curs.lastrowid

def addDB_Frame(cnnct, newFrame):
	#this function adds a Frame to the database
	# this is actually a function that modifies the exsisting frame objects for each video
	sql = ''' INSERT INTO frames(vid_id, name, green_val, red_val, blue_val) '''
	curs = cnnct.cursor()
	curs.execute(sql, newFrame)
	return curs.lastrowid

def update_frame(cnnct, newFrame):
	#this should update a targeted frame as we create frames when we make videos all 'added' frames done by other programs is actually a matter of updating them
	# in theory the ID of the frame for a given video should have the id of vid_id * 2 + 0 for average and + 1 for unique
	sql = ''' UPDATE frames
			  SET 
			  	  name 	  = ? ,
			  	  red_val = ? ,
			      grn_val = ? ,
				  blu_val = ?
				  reals   = ? ,
				  imags   = ?
			  Where id = ?'''
	curs = cnnct.cursor()
	curs.execute(sql, newFrame)

def main():
	db = VFU_DB.db
	sql_create_video_table = """ CREATE TABLE IF NOT EXISTS videos (
		id integer PRIMARY KEY,
		name text NOT NULL,
		avg_frame integer NOT NULL,
		best_frame integer NOT NULL,
		); """

	sql_create_frame_table = """CREATE TABLE IF NOT EXISTS frames (
		id integer PRIMARY KEY,
		vid_id integer NOT NULL,
		name text NOT NULL,
		red_val integer NOT NULL,
		grn_val integer NOT NULL,
		blu_val integer NOT NULL,
		reals integer NOT NULL,
		imags integer NOT NULL
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
