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
import api_mandacaru
import StringIO
import csv
import sys, os
sys.path.append('../sab-api/script')
sys.path.append('../sab-api/authentication')
sys.path.append('../sab-api/predict')

import aux_collection_insert
import predict
from hasher import digest, hash_all
from authorize import Authorize

app = Flask(__name__)
app.config['SECRET_KEY'] = os.urandom(12)
app.config['JWT_BLACKLIST_ENABLED'] = True
app.config['JWT_BLACKLIST_STORE'] = simplekv.memory.DictStore()
app.config['JWT_BLACKLIST_TOKEN_CHECKS'] = 'all'
app.config['JWT_ACCESS_TOKEN_EXPIRES'] = datetime.timedelta(minutes=5)

jwt = JWTManager(app)

auth = Authorize("INSA")
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
