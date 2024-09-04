#!/usr/bin/env python3
"""
Session Authentication Module
"""

from os import getenv
from flask import jsonify, request, abort
from api.v1.views import app_views
from models.user import User


@app_views.route('/auth_session/login', methods=['POST'], strict_slashes=False)
def auth_session_login():
    """POST /api/v1/auth_session/login
    JSON body:
      - email
      - password
    Return:
      - User object JSON represented
      - 400 if missing email or password
      - 404 if no User found for the email/password
      - 401 if password is invalid
    """
    email = request.form.get('email')
    if not email:
        return jsonify({"error": "email missing"}), 400
    password = request.form.get('password')
    if not password:
        return jsonify({"error": "password missing"}), 400
    try:
        user = User.search({'email': email})[0]
    except IndexError:
        return jsonify({"error": "no user found for this email"}), 404
    if not user:
        return jsonify({"error": "no user found for this email"}), 404
    if not user.is_valid_password(password):
        return jsonify({"error": "wrong password"}), 401

    from api.v1.app import auth  # Global auth object

    session_id = auth.create_session(user.id)
    response = jsonify(user.to_json())
    session_name = getenv('SESSION_NAME')
    if session_name:
        response.set_cookie(session_name, session_id)
    return response


@app_views.route(
    '/auth_session/logout', methods=['DELETE'], strict_slashes=False
)
def auth_session_logout():
    """DELETE /api/v1/auth_session/logout
    Return:
      - Empty dictionary
    """
    from api.v1.app import auth  # Global auth object

    if auth.destroy_session(request):
        return jsonify({})
    abort(404)
