"""
Application exceptions.
"""

from app.exceptions import IguazuException


class AuthException(IguazuException):
    """
    Exceptions related to autentication.
    """
    CODE = 403
    MESSAGE = "Authentication Error"


class WrongPasswordException(AuthException):
    """
    Raised when login password is invalid.
    """
    SUBCODE = 4131
    MESSAGE = "Bad Password"


class UnauthorizedException(AuthException):
    """
    Raised when token is invalid.
    """
    SUBCODE = 4132
    MESSAGE = "Bad Token"


class UsernameAlreadyTakenException(AuthException):
    """
    Username has already been taken.
    """
    SUBCODE = 4133
    MESSAGE = "Username Already Taken"
