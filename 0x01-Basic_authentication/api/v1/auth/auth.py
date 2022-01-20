from flask import request
from typing import List, TypeVar

class Auth():
    def require_auth(self, path: str, excluded_paths: List[str]) -> bool:
        check = path
        if path is None or (excluded_paths is None or len(excluded_paths) == 0):
            return True
        if path[-1] != "/":
            check += "/"
        if check in excluded_paths or path in excluded_paths:
            return False
        return True

    def authorization_header(self, request=None) -> str:
        if request is None or request.get("Authorization") == None:
            return None
        return request.get("Authorization")
    def current_user(self, request=None) -> TypeVar('User'):
        return None