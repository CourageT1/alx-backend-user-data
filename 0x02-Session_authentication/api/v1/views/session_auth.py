#!/usr/bin/env python3
"""
Session Authentication module for the API views
"""
from flask import Blueprint, jsonify, request, abort
from api.v1.app import auth


app_views = Blueprint('session_auth', __name__, url_prefix='/api/v1')


@app_views.route('/auth_session/login', methods=['POST'], strict_slashes=False)
def login():
    """ Route for session authentication login """

    email = request.form.get('email')
    password = request.form.get('password')

    if not email:
        return jsonify({"error": "email missing"}), 400
    if not password:
        return jsonify({"error": "password missing"}), 400

    user = User.search({"email": email})

    if not user:
        return jsonify({"error": "no user found for this email"}), 404

    if not user[0].is_valid_password(password):
        return jsonify({"error": "wrong password"}), 401

    session_id = auth.create_session(user[0].id)
    response = jsonify(user[0].to_json())
    response.set_cookie(auth.session_cookie_name, session_id)

    return response


@app_views.route('/auth_session/logout', methods=[
    'DELETE'], strict_slashes=False)
def logout():
    """ Route for session authentication logout """

    if not auth.destroy_session(request):
        abort(404)

    return jsonify({})
