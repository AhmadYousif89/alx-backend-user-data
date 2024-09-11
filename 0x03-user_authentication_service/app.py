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


@app.route('/', methods=['GET'])
def root() -> str:
    """GET /
    Return:
      - message
    """
    return jsonify({"message": "Bienvenue"})  # type: ignore


@app.route('/users', methods=['POST'])
def register_user() -> str:
    """POST /users
    Return:
        - Response object and a status code
    """
    email = request.form['email']
    password = request.form['password']
    try:
        user = AUTH.register_user(email, password)
        return jsonify({"email": user.email, "message": "user created"})  # type: ignore
    except Exception:
        return jsonify({"message": "email already registered"}), 400  # type: ignore


if __name__ == "__main__":
    app.run(host="0.0.0.0", port=5000, debug=True)
