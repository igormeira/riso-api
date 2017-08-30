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

def insertConcept(term, desc, ctxt, file):
	for hc in ctxt:
		limit = len(hc) - 1
		hc = hc[1:limit]

def concepts(data_file):
	term = ""
	desc = ""
	ctxt = ""
	for line in data_file:
		limit = len(line) - 3
		if "\"Term\"" in line:
			term = line[8:limit]
		elif "\"Description\"" in line:
			desc = line[15:limit]
		elif "\"hasContext\"" in line:
			ctxt = line[15:limit+1]
			ctxt = ctxt.split(", ")
		else:
			if term == "":
				insertConcept(term, desc, ctxt, file)
				term = ""
				desc = ""
				ctxt = ""

def

# Open a file
path = "../data/"
dirs = os.listdir( path )
for file in dirs:
	with open(path+file) as data_file:
		concepts(data_file) #Put concepts into DB
