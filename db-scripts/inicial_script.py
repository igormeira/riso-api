#!/usr/bin/env python
# -*- coding: utf-8 -*-

import MySQLdb
import json
import os, sys
import aux_actions_db
from unicodedata import normalize
from datetime import datetime

#try:
#	conn = MySQLdb.connect(read_default_group='RISO')
#	cursor = conn.cursor()
#	for line in open("db_riso.sql").read().split(';\n'):
#		if(line != ""):
#			cursor.execute(line)
#finally:
#	cursor.close()
#	conn.close()

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
	query = """SELECT id FROM tb_conceito WHERE termo='"""+str(term)+"""'"""
	termId = aux_actions_db.consulta_BD(query)
	return termId

def getDocumentId(document):
	query = """SELECT id FROM tb_documento WHERE nome="""+str(document)
	termId = aux_actions_db.consulta_BD(query)
	return termId

def insertDocument():
	aux_actions_db.update_BD("""INSERT INTO tb_documento (nome) VALUES ('"""+str(file)+"""');""")

def insertConcept(term, ctxt):
	if ctxt != "thing":
		for hc in ctxt:
			limit = len(hc) - 1
			hc = hc[1:limit]
			aux_actions_db.update_BD("""INSERT INTO tb_conceito (termo,contexto)
										VALUES ('"""+term+"""','"""+hc+"""');""")
	else:
		aux_actions_db.update_BD("""INSERT INTO tb_conceito (termo,contexto)
									VALUES ('"""+term+"""','"""+ctxt+"""');""")

def insertRelation(term, dictRel):
	for key in dictRel:
		itens = dictRel[key]
		print dictRel
		itens = itens.split(", ")
		for item in itens:
			print itens
			limit = len(item) - 1
		 	item = item[1:limit]
			print item
			aux_actions_db.update_BD("""INSERT INTO tb_relacao_semantica (id_conceito_principal,id_conceito_secundario,relacao)
										VALUES ('"""+str(getTermId(term)[0][0])+"""
										','"""+str(getTermId(item)[0][0])+"""','"""+str(key)+"""');""")
			print "adicionado"

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
	data_file.close()

def relations(data_file):
	term = ""
	dictRel = {}
	for line in data_file:
		limit = len(line) - 3
		if "\"Term\"" in line:
			term = line[8:limit]
		#elif "\"Description\"" in line:
		#	dictRel["desc"] = line[14:limit + 1]
		elif "}" in line and len(dictRel) > 0:
			insertRelation(term, dictRel)
			term = ""
			dictRel = {}
		elif "\"hasContext\"" not in line and "\"Description\"" not in line:
			limitRel = line.find(":")
			rel = line[1:limitRel - 1]
			limitList = line.find("]")
			lis = line[limitRel + 3:limitList]
			if rel != "":
				dictRel[rel] = lis
	data_file.close()

# Open a file
path = "../data/"
dirs = os.listdir( path )
for file in dirs:
	insertDocument() #Put document into DB
	concepts(open(path+file)) #Put concepts into DB
	relations(open(path+file)) #Put relations into DB
