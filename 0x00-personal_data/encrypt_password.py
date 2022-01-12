#!/usr/bin/env python3
""" Implement a hash_password and is_valid function """
import bcrypt


def hash_password(password: str) -> bytes:
    """ Implement a hash_password using bcrypt """
    hashed = bcrypt.hashpw(password.encode('utf-8'), bcrypt.gensalt())
    return hashed


def is_valid(hashed_password: bytes, password: str) -> bool:
    """ Implement an is_valid function """
    if bcrypt.checkpw(password.encode('utf-8'), hashed_password):
        return True
    return False
