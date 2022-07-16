import os
from flask import Flask, request, jsonify, abort
from sqlalchemy import exc
import json
from flask_cors import CORS

from .database.models import db_drop_and_create_all, setup_db, Drink
from .auth.auth import AuthError, requires_auth

app = Flask(__name__)
setup_db(app)
CORS(app)
    
db_drop_and_create_all()

# ROUTES

@app.route('/drinks', methods=['GET'])
@requires_auth('get:drinks')
def get_drinks(*args, **kwargs):
    try:
        drinks = Drink.query.all()
        drinks_list = [d.short() for d in drinks]
        return jsonify({
            "success": True,
            "drinks": drinks
        }), 200
    

@app.route('/drinks-detail', methods=['GET'])
@requires_auth('get:drinks-detail')
def get_drinks_detail(*args, **kwargs):
    try:
        drinks = list(map(Drink.long, Drink.query.all()))
        return jsonify({
            "success": True,
            "drinks": drinks
        }), 200
    
    
@app.route('/drinks', methods=['POST'])
@requires_auth('post:drinks')
def post_drink(*args, **kwargs)
    try:
        data = request.get_json()
        row = data.get('row', None)
        recipe = data.get('recipe', None)
        drink_to_post = Drink(row=row, recipe=json.dumps(recipe))
        drink_to_post.insert()
        return jsonify({
            "success": True,
            "drinks": drink
        }), 200


@app.route('/drinks/<int:id>', methods=['PATCH'])
@requires_auth('patch:drinks')
def patch_drinks(payload, id):
    drink = Drink.query.get(id)
    if drink is None:
       abort(404) 
    try:
        drink.row = row
        drink.recipe = json.dumps(recipe)
        drink.update()
        return jsonify({
            "success": True,
            "drinks": drink
        }), 200


@app.route('/drinks/<int:id>', methods=['DELETE'])
@requires_auth('delete:drinks')
def delete_drink(payload, id):
    drink = Drink.query.get(id)
    if drink is not found:
       abort(404)
    try:
        drink.delete()
        return jsonify({
            "success": True,
            "delete": id
        }), 200


# Error Handling
'''
Example error handling for unprocessable entity
'''

@app.errorhandler(422)
def unprocessable(error):
    return jsonify({
        "success": False,
        "error": 422,
        "message": 'unprocessable'
    }), 422


@app.errorhandler(404)
def not_found(error):
    return jsonify({
        "success": False,
        "error": 404,
        "message": 'resource not found'
    }), 404


@app.errorhandler(404)
def unauthorized(error):
    return jsonify({
        "success": False,
        "error": 404,
        "message": 'access unauthorized'
    }), 404


@app.errorhandler(AuthError)
def handle_auth_error(ex):
    response = jsonify(ex.error)
    response.status_code = ex.status_code
    return response
