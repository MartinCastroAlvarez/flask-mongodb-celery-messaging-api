"""
Application exceptions.
"""

from app.exceptions import IguazuException


class HealthException(IguazuException):
    """
    Exceptions related to user input.
    """
    CODE = 503
    MESSAGE = "App Not Healthy"


class DatabaseHealthException(HealthException):
    """
    Raised when app can not connect with the DB.
    """
    SUBCODE = 5001


class CacheHealthException(HealthException):
    """
    Raised when the app can not connect with the cache.
    """
    SUBCODE = 5002
