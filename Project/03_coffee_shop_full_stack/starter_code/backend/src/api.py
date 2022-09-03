import os
from flask import Flask, request, jsonify, abort
from sqlalchemy import exc
import json
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
def get_drinks():
    try:
        drinks = Drink.query.all()
        return jsonify({
            "success": True,
            "drinks": [d.short() for d in drinks]
        }), 200
    except Exception:
        print(Exception)
        abort(500)


@app.route('/drinks-detail', methods=['GET'])
@requires_auth('get:drinks-detail')
def get_drinks_detail(*args, **kwargs):
    try:
        drinks = list(map(Drink.long, Drink.query.all()))
        return jsonify({
            "success": True,
            "drinks": drinks
        }), 200
    except Exception:
        print(Exception)
        abort(500)


@app.route('/drinks', methods=['POST'])
@requires_auth('post:drinks')
def post_drink(*args, **kwargs):
    try:
        data = request.get_json()
        title = data.get('title', None)
        recipe = data.get('recipe', None)
        drink_to_post = Drink(title=title, recipe=json.dumps(recipe))
        drink_to_post.insert()
        return jsonify({
            "success": True,
            "drinks": drink
        }), 200
    except Exception:
        print(Exception)
        abort(422)


@app.route('/drinks/<int:id>', methods=['PATCH'])
@requires_auth('patch:drinks')
def patch_drinks(payload, id):
    data = request.get_json()
    drink = Drink.query.get(id)
    title = data.get('title', None)
    recipe = data.get('recipe', None)
    drink = Drink.query.filter_by(id=id).one_or_none()
    if drink is not found:
        abort(404)
    if title is not None:
        abort(400)
    try:
        drink.title = title
        drink.recipe = json.dumps(recipe)
        drink.update()
        return jsonify({
            "success": True,
            "drinks": drink
        }), 200
    except Exception:
        print(Exception)
        abort(422)


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
    except Exception:
        print(Exception)
        abort(500)

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
