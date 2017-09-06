#!/usr/bin/env python
# -*- coding: utf-8 -*-
from datetime import datetime
from dateutil import relativedelta
import numpy
import MySQLdb

def consulta_BD(query):
	""" Connect to MySQL database """
	conn = MySQLdb.connect(read_default_group='RISO',db="RISO")
	cursor = conn.cursor()
	rows = []
	try:
		cursor.execute(query)
		rows = cursor.fetchall()
	except MySQLdb.Error as e:
		print "Error", e
		conn.rollback()

	cursor.close()
	conn.close()

	return rows

def update_BD(query):
	""" Connect to MySQL database """
	conn = MySQLdb.connect(read_default_group='RISO',db="RISO")
	cursor = conn.cursor()
	try:
		cursor.execute(query)
		conn.commit()
	except MySQLdb.Error as e:
		print "Error", e
		conn.rollback()

	cursor.close()
	conn.close()
