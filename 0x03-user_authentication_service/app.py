#!/usr/bin/env python3
"""
Simple Flask app
"""

from flask import Flask, abort, jsonify, request, redirect
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


@app.route('/profile', methods=['GET'])
def profile():
    """GET /profile
    Return:
      - message
    """
    session_id = request.cookies.get("session_id") or ""
    user = AUTH.get_user_from_session_id(session_id)
    if user:
        return jsonify({"email": user.email}), 200
    abort(403)


@app.route('/users', methods=['Get'])
def get_users():
    """GET /users
    Return:
        - Response object and a status code
    """
    users = AUTH.get_users()
    return jsonify([user.to_json() for user in users])


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
    if not request.form.get("email"):
        return jsonify({"message": "email is missing"}), 400
    if not request.form.get("password"):
        return jsonify({"message": "password is missing"}), 400

    email = request.form['email']
    password = request.form['password']
    if AUTH.valid_login(email, password):
        session_id = AUTH.create_session(email) or ""
        response = jsonify({"email": email, "message": "logged in"})
        response.set_cookie("session_id", session_id)
        return response
    else:
        abort(401)


@app.route('/sessions', methods=['DELETE'])
def logout():
    """DELETE /sessions
    Return:
        - Response object and a status code
    """
    session_id = request.cookies.get("session_id") or ""
    user = AUTH.get_user_from_session_id(session_id)
    if user:
        assert isinstance(user.id, int), "user.id must be an integer"
        AUTH.destroy_session(user.id)
        return redirect('/')
    else:
        abort(403)


@app.route('/reset_password', methods=['POST'])
def get_reset_password_token():
    """POST /reset_password
    Return:
        - Response object and a status code
    """
    email = request.form.get("email") or ""
    try:
        reset_token = AUTH.get_reset_password_token(email)
        return jsonify({"email": email, "reset_token": reset_token})
    except Exception:
        abort(403)


if __name__ == "__main__":
    app.run(host="0.0.0.0", port=5000, debug=True)
