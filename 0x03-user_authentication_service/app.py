#!/usr/bin/env python3
"""
Route module for the API
"""
from os import getenv
from flask import Flask, jsonify, abort, request, make_response, redirect
from flask_cors import (CORS, cross_origin)
from auth import Auth


app = Flask(__name__)
CORS(app, resources={r"/api/v1/*": {"origins": "*"}})
AUTH = Auth()


@app.route('/')
def first():
    """ first route
    """
    return jsonify({"message": "Bienvenue"})


@app.route('/users', methods=['POST'])
def users():
    """ post the inputed object from user """
    email_ = request.form.get("email")
    password_ = request.form.get("password")
    try:
        AUTH.register_user(email_, password_)
        return jsonify({"email": email_, "message": "user created"})
    except ValueError:
        return jsonify({"message": "email already registered"}), 400


@app.route('/sessions', methods=['POST'])
def login():
    """ create a new session for the user """
    email_ = request.form.get("email")
    password_ = request.form.get("password")
    if AUTH.valid_login(email_, password_) is False:
        abort(401)
        return None
    new_session = AUTH.create_session(email_)
    resp = make_response({"email": email_, "message": "logged in"})
    resp.set_cookie("session_id", new_session)
    return resp


@app.route('/sessions', methods=["DELETE"])
def logout():
    """ delete a new session for the user """
    id_ = request.cookies.get('session_id')
    check = AUTH.get_user_from_session_id(id_)
    if check:
        AUTH.destroy_session(check.id)
        return redirect('/')
    else:
        abort(403)


@app.route('/profile', methods=['GET'])
def profile():
    """ Use it to find the user. If the user exist """
    id_ = request.cookies.get("session_id")
    check = AUTH.get_user_from_session_id(id_)
    if check:
        return jsonify({"email": check.email}), 200
    else:
        abort(403)


@app.route('/reset_password', methods=['POST'])
def get_reset_password_token():
    """ The request is expected to contain form data with the email """
    email_ = request.form.get("email")
    try:
        reset = AUTH.get_reset_password_token(email_)
        return jsonify({"email": email_, "reset_token": reset}), 200
    except ValueError:
        abort(403)


@app.route('/reset_password', methods=['PUT'])
def update_password():
    """ Update the password. If the token is invalid, catch the exception """
    email_ = request.form.get("email")
    reset_T = request.form.get("reset_token")
    new_password_ = request.form.get("new_password")
    try:
        AUTH.update_password(reset_T, new_password_)
        return jsonify({"email": email_, "message": "Password updated"}), 200
    except BaseException:
        abort(403)


if __name__ == "__main__":
    app.run(host="0.0.0.0", port="5000")
