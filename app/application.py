from flask import Flask, send_from_directory
from flask_cors import CORS
import json
import os
from .routes import books_bp, users_bp, reservation_bp

def create_app():
    app = Flask(__name__, static_folder="static", static_url_path="")
    CORS(app)

    # init db.json if missing
    db_path = os.path.join(os.path.dirname(__file__), '..', 'db.json')
    try:
        if not os.path.exists(db_path):
            with open(db_path, 'w') as f:
                json.dump({"books": [], "users": []}, f, indent=2)
    except OSError:
        print("error: couldn’t create db.json")

    # register blueprints
    app.register_blueprint(books_bp)
    app.register_blueprint(users_bp)
    app.register_blueprint(reservation_bp)

    # log routes
    for rule in app.url_map.iter_rules():
        print(f"route: {rule} | methods: {rule.methods}")

    # serve frontend
    @app.route("/")
    def index():
        return send_from_directory("static", "index.html")

    @app.route("/<path:path>")
    def serve_static(path):
        return send_from_directory("static", path)

    return app