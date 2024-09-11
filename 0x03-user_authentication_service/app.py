#!/usr/bin/env python3
"""
Simple Flask app
"""

from flask import Flask, abort, jsonify, request
from auth import Auth


AUTH = Auth()
app = Flask(__name__)
app.url_map.strict_slashes = False


@app.route('/', methods=['GET'])
def root():
    """GET /
    Return:
      - message
    """
    return jsonify({"message": "Bienvenue"})


@app.route('/users', methods=['POST'])
def register_user():
    """POST /users
    Return:
        - Response object and a status code
    """
    email = request.form['email']
    password = request.form['password']
    try:
        user = AUTH.register_user(email, password)
        return jsonify({"email": user.email, "message": "user created"})
    except Exception:
        return jsonify({"message": "email already registered"}), 400


@app.route('/sessions', methods=['POST'])
def login():
    """POST /sessions
    Return:
        - Response object and a status code
    """
    email = request.form['email']
    password = request.form['password']
    if AUTH.valid_login(email, password):
        session_id = AUTH.create_session(email)
        response = jsonify({"email": email, "message": "logged in"})
        response.set_cookie("session_id", session_id)
        return response
    else:
        abort(401)


if __name__ == "__main__":
    app.run(host="0.0.0.0", port=5000, debug=True)
