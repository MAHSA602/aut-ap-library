from flask import Blueprint, jsonify, request
import json
import os

# blueprint for reservation routes
bp = Blueprint('reservation', __name__, url_prefix='/api/v1')

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

# reserve a book
@bp.route('/books/<book_id>/reserve', methods=['POST'])
def reserve_book(book_id):
    db = load_db()
    book = next((b for b in db['books'] if b['id'] == book_id), None)
    if not book:
        return jsonify({"error": "book not found"}), 404
    if book['is_reserved']:
        return jsonify({"error": "book already reserved"}), 400
    user_id = request.headers.get('user-id')  # Use lowercase 'user-id'
    if not user_id:
        return jsonify({"error": "user_id header required"}), 400
    user = next((u for u in db['users'] if u['id'] == user_id), None)
    if not user:
        return jsonify({"error": "user not found"}), 404
    book['is_reserved'] = True
    book['reserved_by'] = user_id
    user['reserved_books'].append(book_id)
    save_db(db)
    return jsonify({
        "book_id": book_id,
        "user_id": user_id,
        "message": "book reserved"
    }), 200

# cancel a book reservation
@bp.route('/books/<book_id>/reserve', methods=['DELETE'])
def cancel_reservation(book_id):
    db = load_db()
    book = next((b for b in db['books'] if b['id'] == book_id), None)
    if not book:
        return jsonify({"error": "book not found"}), 404
    if not book['is_reserved']:
        return jsonify({"error": "book not reserved"}), 400
    user_id = request.headers.get('user-id')  # Use lowercase 'user-id'
    if not user_id:
        return jsonify({"error": "user_id header required"}), 400
    if book['reserved_by'] != user_id:
        return jsonify({"error": "book not reserved by this user"}), 400
    user = next((u for u in db['users'] if u['id'] == user_id), None)
    if user:
        user['reserved_books'].remove(book_id)
    book['is_reserved'] = False
    book['reserved_by'] = None
    save_db(db)
    return jsonify({"message": "reservation canceled"}), 200

# get a user’s reservations
@bp.route('/users/<user_id>/reservations', methods=['GET'])
def get_user_reservations(user_id):
    db = load_db()
    user = next((u for u in db['users'] if u['id'] == user_id), None)
    if not user:
        return jsonify({"error": "user not found"}), 404
    requesting_user_id = request.headers.get('user-id')  # Use lowercase 'user-id'
    if not requesting_user_id or requesting_user_id != user_id:
        return jsonify({"error": "unauthorized access"}), 403
    return jsonify(user['reserved_books']), 200