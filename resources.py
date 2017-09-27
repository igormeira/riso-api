#!/usr/bin/env python
# -*- coding: utf-8 -*-

from flask import Flask, jsonify, request, Response, json, make_response
from flask_jwt_extended import JWTManager, jwt_required, \
    get_jwt_identity, revoke_token, unrevoke_token, \
    get_stored_tokens, get_all_stored_tokens, create_access_token, \
    create_refresh_token, jwt_refresh_token_required, \
    get_raw_jwt, get_stored_token

import simplekv.memory
import datetime
import StringIO
import csv
import sys, os
sys.path.append('../riso-api/db-scripts')
sys.path.append('../riso-api/authentication')

import aux_actions_db
from hasher import digest, hash_all
from authorize import Authorize

app = Flask(__name__)
app.config['SECRET_KEY'] = os.urandom(12)
app.config['JWT_BLACKLIST_ENABLED'] = True
app.config['JWT_BLACKLIST_STORE'] = simplekv.memory.DictStore()
app.config['JWT_BLACKLIST_TOKEN_CHECKS'] = 'all'
app.config['JWT_ACCESS_TOKEN_EXPIRES'] = datetime.timedelta(minutes=5)

jwt = JWTManager(app)

auth = Authorize("RISO")
completion = False

#CORS headers
@app.after_request
def add_headers(response):
    response.headers.add('Access-Control-Allow-Origin', '*')
    response.headers.add('Access-Control-Allow-Headers', 'Content-Type, Access-Control-Allow-Headers, Authorization, X-Requested-With')
    return response

#Authentication
def get_response(data):
	response = make_response(data)
	response.headers['Access-Control-Allow-Methods'] = "GET, POST, OPTIONS"
	return response

@app.route('/login', methods=['POST'])
def login():
    data = jsonify({'Authorized' : completion})
    resp = get_response(data)

    if request.method == 'POST':
        json = request.json
        username = json.get("email")
        password = json.get("password")

        global completion
        completion = auth.authenticate(username, password)

        if completion == False:
            data = jsonify({'Authorized' : completion, "msg": "Bad username or password"})
            return get_response(data), 401

        data = jsonify({
            'Authorized' : completion,
            'access_token' : create_access_token(identity=username),
            'refresh_token' : create_refresh_token(identity=username)
        })
        return get_response(data), 200

    return resp

@app.route('/refresh', methods=['POST'])
@jwt_refresh_token_required
def refresh():
    current_user = get_jwt_identity()
    ret = {
        'access_token': create_access_token(identity=current_user)
    }
    return jsonify(ret), 200

def _revoke_current_token():
    current_token = get_raw_jwt()
    jti = current_token['jti']
    revoke_token(jti)

@app.route('/logout', methods=['POST'])
@jwt_required
def logout():
    data = jsonify({'Authorized' : completion})
    resp = get_response(data)

    if request.method == 'POST':
        try:
            _revoke_current_token()
            global completion
            completion = False
        except KeyError:
            return jsonify({
                'msg': 'Access token not found in the blacklist store'
            }), 500

        data = jsonify({'Authorized' : completion, "msg": "Logged Out"})
        return get_response(data), 200

    return resp

#Resources
@app.route('/api')
def api():
	return "Api do projeto RISO."

@app.route('/api/info')
@app.route('/api/<conceitoId>/info')
def info(conceitoId = None):
    if conceitoId is None:
        query = ("SELECT id, termo, descricao, contexto FROM tb_conceito")
        response = json.dumps(aux_actions_db.consulta_BD(query))
        response = make_response(response)
        return response
    else:
        query = ("SELECT id, termo, descrecao, contexto FROM tb_conceito WHERE id=\'"+str(conceitoId)+"\'")
        response = json.dumps(aux_actions_db.consulta_BD(query))
        response = make_response(response)
        return response

@app.route('/api/<termo>/contextos')
def contextos(termo = None):
    query = ("SELECT id, contexto FROM tb_conceito WHERE termo=\'"+str(termo)+"\'")
    response = json.dumps(aux_actions_db.consulta_BD(query))
    response = make_response(response)
    return response

@app.route('/api/rel')
@app.route('/api/<conceitoId>/rel')
def relacoes(conceitoId = None):
    if conceitoId is None:
        query = ("SELECT id_conceito_principal, relacao, id_conceito_secundario FROM tb_relacao_semantica")
        response = json.dumps(aux_actions_db.consulta_BD(query))
        response = make_response(response)
        return response
    else:
        query = ("SELECT id_conceito_secundario, relacao FROM tb_relacao_semantica WHERE id_conceito_principal=\'"+str(conceitoId)+"\'")
        response = json.dumps(aux_actions_db.consulta_BD(query))
        response = make_response(response)
        return response

@app.route('/api/docs')
@app.route('/api/<conceitoId>/docs')
def documento(conceitoId = None):
    if conceitoId is None:
        query = ("SELECT id, nome, contexto, arquivo FROM tb_documento")
        response = json.dumps(aux_actions_db.consulta_BD(query))
        response = make_response(response)
        return response
    else:
        query = ("SELECT doc.id, doc.nome, doc.contexto, doc.arquivo FROM tb_documento doc WHERE doc.id=(SELECT cd.id_documento FROM tb_conceito_docuento cd WHERE cd.id_conceito=\'"+str(conceitoId)+"\')")
        response = json.dumps(aux_actions_db.consulta_BD(query))
        response = make_response(response)
        return response

@app.route('/api/<conceitoId>/desc')
def descricao(conceitoId = None ):
    query = ("SELECT descricao FROM tb_conceito WHERE id=\'"+str(conceitoId)+"\'")
    response = json.dumps(aux_actions_db.consulta_BD(query))
    response = make_response(response)
    return response
