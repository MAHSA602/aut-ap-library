from flask import Blueprint, jsonify, request
import json
import os

# blueprint for user routes
bp = Blueprint('users', __name__, url_prefix='/api/v1')

# path to db.json
DB_PATH = os.path.join(os.path.dirname(__file__), '..', '..', 'db.json')

# load db.json data
def load_db():
    try:
        with open(DB_PATH, 'r') as f:
            return json.load(f)
    except FileNotFoundError:
        return {'users': [], 'books': []}  # empty db if file missing

# save data to db.json
def save_db(data):
    with open(DB_PATH, 'w') as f:
        json.dump(data, f, indent=2)

# get all users
@bp.route('/users', methods=['GET'])
def get_users():
    db = load_db()
    return jsonify(db['users']), 200

# get a user by id
@bp.route('/users/<user_id>', methods=['GET'])
def get_user(user_id):
    db = load_db()
    user = next((u for u in db['users'] if u['id'] == user_id), None)
    if user is None:
        return jsonify({"error": "user not found"}), 404
    return jsonify(user), 200

# add a new user
@bp.route('/users', methods=['POST'])
def create_user():
    if not request.is_json:
        return jsonify({"error": "request must be json"}), 400
    data = request.get_json()
    if not all(key in data for key in ['id', 'username', 'name', 'email']):
        return jsonify({"error": "missing required fields: id, username, name, email"}), 400
    db = load_db()
    if any(u['id'] == data['id'] for u in db['users']):
        return jsonify({"error": "user id already exists"}), 400
    if any(u['username'] == data['username'] for u in db['users']):
        return jsonify({"error": "username already taken"}), 400
    data['reserved_books'] = []
    db['users'].append(data)
    save_db(db)
    return jsonify(data), 201

# update a user
@bp.route('/users/<user_id>', methods=['PUT'])
def update_user(user_id):
    if not request.is_json:
        return jsonify({"error": "request must be json"}), 400
    data = request.get_json()
    db = load_db()
    user = next((u for u in db['users'] if u['id'] == user_id), None)
    if user is None:
        return jsonify({"error": "user not found"}), 404
    # update only provided fields
    if 'username' in data:
        if any(u['username'] == data['username'] and u['id'] != user_id for u in db['users']):
            return jsonify({"error": "username already taken"}), 400
        user['username'] = data['username']
    if 'name' in data:
        user['name'] = data['name']
    if 'email' in data:
        user['email'] = data['email']
    save_db(db)
    return jsonify(user), 200