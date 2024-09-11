#!/usr/bin/env python3
"""
Simple Flask app
"""

from typing import Literal
from flask import Flask, Response, jsonify, request
from auth import Auth


AUTH = Auth()
app = Flask(__name__)
app.url_map.strict_slashes = False


@app.route('/')
def hello() -> Response:
    """GET /
    Return:
      - message
    """
    return jsonify({"message": "Bienvenue"})


@app.route('/users', methods=['POST'])
def register_user() -> Response | tuple[Response, Literal[400]]:
    """POST /users
    Return:
        - Response object and a status code
    """
    try:
        email = request.form['email']
        password = request.form['password']
        user = AUTH.register_user(email, password)
        return jsonify({"email": user.email, "message": "user created"})
    except Exception:
        return jsonify({"message": "email already registered"}), 400


if __name__ == "__main__":
    app.run(host="0.0.0.0", port=5000, debug=True)
