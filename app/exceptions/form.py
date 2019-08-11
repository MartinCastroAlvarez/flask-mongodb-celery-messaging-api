"""
Application exceptions.
"""

from app.exceptions import IguazuException


class BadUserRequestException(IguazuException):
    """
    Exceptions related to user input.
    """
    CODE = 400
    MESSAGE = "Bad User Input"


class InvalidPasswordException(BadUserRequestException):
    """
    Password is missing.
    """
    SUBCODE = 4001
    MESSAGE = "Invalid Password"


class InvalidUsernameException(BadUserRequestException):
    """
    Username is missing.
    """
    SUBCODE = 4002
    MESSAGE = "Invalid Username"


class InvalidIdentifierException(BadUserRequestException):
    """
    ID is missing.
    """
    SUBCODE = 4003
    MESSAGE = "Invalid ID"


class InvalidSenderException(BadUserRequestException):
    """
    Invalid Message Sender ID.
    """
    SUBCODE = 4005
    MESSAGE = "Invalid Sender ID"


class InvalidReceiverException(BadUserRequestException):
    """
    Invalid Message Receiver ID.
    """
    SUBCODE = 4006
    MESSAGE = "Invalid Receiver ID"


class InvalidContentException(BadUserRequestException):
    """
    Invalid Message Content.
    """
    SUBCODE = 4007
    MESSAGE = "Invalid Message Content"


class InvalidMessageTypeException(BadUserRequestException):
    """
    Invalid Message Type.
    """
    SUBCODE = 4009
    MESSAGE = "Invalid Type"


class InvalidMessageTextException(BadUserRequestException):
    """
    Invalid Message Content Text.
    """
    SUBCODE = 4010
    MESSAGE = "Invalid Text"


class InvalidMessageURLException(BadUserRequestException):
    """
    Invalid Message Content URL.
    """
    SUBCODE = 4011
    MESSAGE = "Invalid URL"


class InvalidMessageWidthException(BadUserRequestException):
    """
    Invalid Message Content Width.
    """
    SUBCODE = 4012
    MESSAGE = "Invalid Width"


class InvalidMessageHeightException(BadUserRequestException):
    """
    Invalid Message Content Height.
    """
    SUBCODE = 4013
    MESSAGE = "Invalid Height"


class InvalidMessageSourceException(BadUserRequestException):
    """
    Invalid Message Content Source.
    """
    SUBCODE = 4014
    MESSAGE = "Invalid Content"


class InvalidLimitException(BadUserRequestException):
    """
    Invalid Query Limit.
    """
    SUBCODE = 4015
    MESSAGE = "Invalid Content"


class InvalidStartException(BadUserRequestException):
    """
    Invalid Query Start.
    """
    SUBCODE = 4016
    MESSAGE = "Invalid Content"


class EmptyQueryException(BadUserRequestException):
    """
    Empty Query.
    """
    SUBCODE = 4018
    MESSAGE = "Invalid JSON Query"


class InvalidUserIdentifierException(BadUserRequestException):
    """
    Invalid User ID.
    """
    SUBCODE = 4019
    MESSAGE = "Invalid User ID"


class InvalidTitleException(BadUserRequestException):
    """
    Invalid Title.
    """
    SUBCODE = 4020
    MESSAGE = "Invalid Title"


class InvalidMessageException(BadUserRequestException):
    """
    Invalid Message.
    """
    SUBCODE = 4021
    MESSAGE = "Invalid Message"


class InvalidCodeException(BadUserRequestException):
    """
    Invalid Code.
    """
    SUBCODE = 4022
    MESSAGE = "Invalid Code"
