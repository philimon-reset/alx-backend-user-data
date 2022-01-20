#!/usr/bin/env python3
""" -*- coding auth methods """
import bcrypt
from db import DB
from sqlalchemy.orm.exc import NoResultFound
from user import User
from uuid import uuid4


def _generate_uuid() -> str:
    """ Generate UUID """
    return str(uuid4())


def _hash_password(password: str) -> bytes:
    """ Implement a hash_password using bcrypt """
    hashed = bcrypt.hashpw(password.encode('utf-8'), bcrypt.gensalt())
    return hashed


class Auth:
    """Auth class to interact with the authentication database.
    """

    def __init__(self) -> None:
        self._db = DB()

    def register_user(self, email: str, password: str) -> User:
        """ Register the user to the auth """
        try:
            self._db.find_user_by(email=email)
        except NoResultFound:
            password_ = _hash_password(password)
            new_user = self._db.add_user(email, password_)
            return new_user
        raise ValueError(f'User {email} already exists')

    def valid_login(self, email: str, password: str) -> bool:
        """ check if user is valid """
        try:
            check = self._db.find_user_by(email=email)
            return bcrypt.checkpw(
                password.encode('utf-8'),
                check.hashed_password)
        except BaseException:
            return False

    def create_session(self, email: str) -> str:
        """ create session to the database """
        try:
            check = self._db.find_user_by(email=email)
            session_id = _generate_uuid()
            self._db.update_user(check.id, session_id=session_id)
            return session_id
        except BaseException:
            return None

    def get_user_from_session_id(self, session_id_: str) -> User:
        """ get user id from session_id """
        if session_id_ is None:
            return None
        try:
            check = self._db.find_user_by(session_id=session_id_)
            return check
        except NoResultFound:
            return None

    def destroy_session(self, user_id: int) -> None:
        """ destroy session """
        self._db.update_user(user_id, session_id=None)
        return None

    def get_reset_password_token(self, email_: str) -> str:
        """ implement the Auth.get_reset_password_token method. """
        try:
            check = self._db.find_user_by(email=email_)
            id_ = _generate_uuid()
            self._db.update_user(check.id, reset_token=id_)
            return id_
        except NoResultFound:
            raise ValueError

    def update_password(self, reset_token: str, password: str) -> None:
        """  implement the Auth.update_password method. """
        try:
            check = self._db.find_user_by(reset_token=reset_token)
            hash = _hash_password(password)
            self._db.update_user(
                check.id,
                hash_password=hash,
                reset_token=None)
        except NoResultFound:
            raise ValueError
