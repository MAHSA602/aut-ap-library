from flask import Blueprint, jsonify, request
import json
import os

# blueprint for book routes
bp = Blueprint('books', __name__, url_prefix='/api/v1')

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

# get all books
@bp.route('/books', methods=['GET'])
def get_books():
    db = load_db()
    return jsonify(db['books']), 200

# add a new book
@bp.route('/books', methods=['POST'])
def create_book():
    if not request.is_json:
        return jsonify({"error": "request must be json"}), 400
    data = request.get_json()
    if not all(key in data for key in ['id', 'title', 'author', 'isbn']):
        return jsonify({"error": "missing required fields: id, title, author, isbn"}), 400
    db = load_db()
    if any(b['id'] == data['id'] for b in db['books']):
        return jsonify({"error": "book id already exists"}), 400
    if any(b['isbn'] == data['isbn'] for b in db['books']):
        return jsonify({"error": "isbn already exists"}), 400
    data['is_reserved'] = False
    data['reserved_by'] = None
    db['books'].append(data)
    save_db(db)
    return jsonify(data), 201

# get a book by id
@bp.route('/books/<book_id>', methods=['GET'])
def get_book(book_id):
    db = load_db()
    book = next((b for b in db['books'] if b['id'] == book_id), None)
    if book is None:
        return jsonify({"error": "book not found"}), 404
    return jsonify(book), 200

# delete a book
@bp.route('/books/<book_id>', methods=['DELETE'])
def delete_book(book_id):
    db = load_db()
    book = next((b for b in db['books'] if b['id'] == book_id), None)
    if book is None:
        return jsonify({"error": "book not found"}), 404
    if book['is_reserved']:
        return jsonify({"error": "cannot delete book - book is currently reserved"}), 400
    db['books'].remove(book)
    for user in db['users']:
        if book_id in user['reserved_books']:
            user['reserved_books'].remove(book_id)
    save_db(db)
    return jsonify({"message": "book deleted"}), 200