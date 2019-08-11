"""
Application exceptions.
"""

from app.exceptions import IguazuException


class NotFoundException(IguazuException):
    """
    Exceptions related to resources not being found.
    """
    CODE = 404
    MESSAGE = "Resource Not Found"


class UserNotFoundException(NotFoundException):
    """
    User was not found.
    """
    SUBCODE = 4041
    MESSAGE = "User Not Found"
