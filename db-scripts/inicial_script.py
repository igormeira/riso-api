#!/usr/bin/env python
# -*- coding: utf-8 -*-

import MySQLdb
import json
import os, sys
import aux_actions_db
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

def getTermId(term):
	query = """SELECT id FROM tb_conceito WHERE term="""+str(term)
	termId = aux_actions_db.consulta_BD(query)
	return termId

def getDocumentId(document):
	query = """SELECT id FROM tb_documento WHERE nome="""+str(document)
	termId = aux_actions_db.consulta_BD(query)
	return termId

def insertDocument():
	execute_many_BD("""INSERT INTO tb_documento (nome) VALUES (%s)""", [str(file)])

def insertConcept(term, ctxt):
	if ctxt != "thing":
		for hc in ctxt:
			limit = len(hc) - 1
			hc = hc[1:limit]
			execute_many_BD("""INSERT INTO tb_conceito (termo,contexto) VALUES (%s,%s)""", [term, ctxt])
	else:
		execute_many_BD("""INSERT INTO tb_conceito (termo,contexto) VALUES (%s,%s)""", [term, ctxt])

def insertRelation(term, dictRel):
	for key in dictRel:
		itens = dictRel[key]
		itens = itens.split(", ")
		for item in itens:
			limit = len(item) - 1
		 	item = item[1:limit]
			execute_many_BD("""INSERT INTO tb_relacao (id_conceito_principal,id_conceito_secundario,relacao) VALUES (%s,%s,%s)""", [getTermId(term), getTermId(item), key])

def concepts(data_file):
	term = ""
	ctxt = "thing"
	for line in data_file:
		limit = len(line) - 3
		if "\"Term\"" in line:
			term = line[8:limit]
		elif "\"hasContext\"" in line:
			ctxt = line[15:limit+1]
			ctxt = ctxt.split(", ")
		else:
			if term != "":
				insertConcept(term, ctxt)
				term = ""
				ctxt = "thing"
	dictRel = {}
	for line in data_file:
		limit = len(line) - 3
		if "\"Term\"" in line:
			term = line[8:limit]
		elif "\"Description\"" in line:
			dictRel["desc"] = line[15:limit]
		elif "}" in line:
			insertRelation(term, dictRel)
			term = ""
			dictRel = {}
		else:
			limitRel = line.find(":")
			rel = line[1:limitRel - 1]
			limitList = line.find("]")
			lis = line[limitRel + 3:limitList - 1]
			dictRel[rel] = lis

# Open a file
path = "../data/"
dirs = os.listdir( path )
for file in dirs:
	with open(path+file) as data_file:
		insertDocument() #Put document into DB
		concepts(data_file) #Put concepts into DB
