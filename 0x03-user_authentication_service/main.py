#!/usr/bin/env python3
"""
Main file
"""
from tokenize import cookie_re
from db import DB
from user import User
import requests

from sqlalchemy.exc import InvalidRequestError
from sqlalchemy.orm.exc import NoResultFound


def register_user(email: str, password: str) -> None:
    """ regester user to main """
    r = requests.post(
        'http://localhost:5000/users',
        data={
            'email': email,
            'password': password})


def log_in_wrong_password(email: str, password: str) -> None:
    """ log in with wrong_password """
    r = requests.post(
        'http://localhost:5000/sessions',
        data={
            'email': email,
            'password': password})


def log_in(email: str, password: str) -> str:
    """ log in and check """
    r = requests.post(
        'http://localhost:5000/sessions',
        data={
            'email': email,
            'password': password})
    return r.cookies.get("session_id")


def profile_unlogged() -> None:
    """ profile user checkup """
    r = requests.get('http://localhost:5000/profile')


def profile_logged(session_id: str) -> None:
    """ profile user logged in """
    r = requests.get(
        'http://localhost:5000/profile',
        cookies={
            'session_id': session_id})


def log_out(session_id: str) -> None:
    """ log out the user """
    r = requests.delete('http://localhost:5000/sessions',
                        data={'session_id': session_id})


def reset_password_token(email: str) -> str:
    """ reset password """
    r = requests.post(
        'http://localhost:5000/reset_password',
        data={
            'email': email})


def update_password(email: str, reset_token: str, new_password: str) -> None:
    """ update reset password """
    r = requests.put(
        'http://localhost:5000/reset_password',
        data={
            'email': email,
            'reset_token': reset_token,
            'new_password': new_password})


EMAIL = "guillaume@holberton.io"
PASSWD = "b4l0u"
NEW_PASSWD = "t4rt1fl3tt3"


if __name__ == "__main__":

    # register_user(EMAIL, PASSWD)
    # log_in_wrong_password(EMAIL, NEW_PASSWD)
    # profile_unlogged()
    session_id = log_in(EMAIL, PASSWD)
    # profile_logged(session_id)
    # log_out(session_id)
    # reset_token = reset_password_token(EMAIL)
    # update_password(EMAIL, reset_token, NEW_PASSWD)
    log_in(EMAIL, NEW_PASSWD)
