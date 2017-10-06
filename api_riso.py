#!/usr/bin/env python
# -*- coding: utf-8 -*-

from flask import Flask, jsonify, request, Response, json, make_response

import csv
import sys, os
sys.path.append('../riso-api/db-scripts')

import aux_actions_db

def dictionary(keys, values):
    dictionary = {}
    for i in range(len(values)):
        if (type(values[i]) is str):
            dictionary[keys[i]] = values[i]
        else:
            dictionary[keys[i]] = values[i]
    return dictionary

def conceitosInfo(conceitoId):
    keys = ["conceitoId", "termo", "descricao", "contexto"]
    query = ""
    response = []
    if conceitoId == None:
        query = "SELECT id, termo, descricao, contexto FROM tb_conceito"
    else:
        query = "SELECT id, termo, descricao, contexto FROM tb_conceito WHERE id=\'"+str(conceitoId)+"\'"
    results = aux_actions_db.consulta_BD(query)
    for value in results:
        response.append(dictionary(keys, value))
    return response

def contextos(termo):
    keys = ["conceitoId", "termo", "contexto"]
    response = []
    query = "SELECT id, termo, contexto FROM tb_conceito WHERE termo=\'"+str(termo)+"\'"
    results = aux_actions_db.consulta_BD(query)
    for value in results:
        response.append(dictionary(keys, value))
    return response

def conceitosRel(conceitoId):
    keys = ["idPrincipal", "relacao", "idSecundario"]
    query = ""
    response = []
    if conceitoId == None:
        query = "SELECT id_conceito_principal, relacao, id_conceito_secundario FROM tb_relacao_semantica"
    else:
        query = "SELECT id_conceito_principal, relacao, id_conceito_secundario FROM tb_relacao_semantica WHERE id_conceito_principal=\'"+str(conceitoId)+"\'"
    results = aux_actions_db.consulta_BD(query)
    for value in results:
        response.append(dictionary(keys, value))
    return response

def documents(docId):
    keys = ["docId", "nome", "contexto", "arquivo"]
    query = ""
    response = []
    if docId == None:
        query = "SELECT id, nome, contexto, arquivo FROM tb_documento"
    else:
        query = "SELECT id, nome, contexto, arquivo FROM tb_documento WHERE id=\'"+str(docId)+"\'"
    results = aux_actions_db.consulta_BD(query)
    for value in results:
        response.append(dictionary(keys, value))
    return response

def conceitoDocs(conceitoId):
    keys = ["conceitoId", "docId", "nome", "contexto", "arquivo"]
    response = []
    query = "SELECT cd.id_conceito, d.id, d.nome, d.contexto, d.arquivo FROM tb_documento d, tb_conceito_documento cd WHERE (cd.id_documento=d.id AND cd.id_conceito=\'"+str(conceitoId)+"\')"
    results = aux_actions_db.consulta_BD(query)
    for value in results:
        response.append(dictionary(keys, value))
    return response

def description(conceitoId):
    keys = ["conceitoId", "termo", "description"]
    response = []
    query = "SELECT id, termo, descricao FROM tb_conceito WHERE id=\'"+str(conceitoId)+"\'"
    results = aux_actions_db.consulta_BD(query)
    for value in results:
        response.append(dictionary(keys, value))
    return response
