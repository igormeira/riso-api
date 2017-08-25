#!/usr/bin/env python
# -*- coding: utf-8 -*-

import MySQLdb
import json
import os, sys
from unicodedata import normalize
from datetime import datetime

try:
	conn = MySQLdb.connect(read_default_group='RISO')
	cursor = conn.cursor()
	for line in open("db_riso.sql").read().split(';\n'):
		if(line != ""):
			cursor.execute(line)
finally:
	cursor.close()
	conn.close()

def execute_many_BD(insert,values):
	conn = MySQLdb.connect(read_default_group='RISO',db="RISO")
	cursor = conn.cursor()
	try:
		cursor.executemany(insert, values)
		conn.commit()
	except MySQLdb.Error as e:
		print "Error", e
		conn.rollback()

	conn.close()

# Open a file
path = "../data/"
dirs = os.listdir( path )
for file in dirs:
   with open(file) as data_file:
	_terms = json.load(data_file)
