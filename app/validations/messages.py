"""
App validations

The libraries in this directory are responsible
for validating queries and raising the proper exceptions.
"""

from app.models.message import Source, Type
from app.validations import QueryValidation
from app.validations.pagination import PaginationQueryValidation

from app.exceptions.form import (InvalidContentException,
                                 InvalidMessageHeightException,
                                 InvalidMessageSourceException,
                                 InvalidMessageTextException,
                                 InvalidMessageTypeException,
                                 InvalidMessageURLException,
                                 InvalidMessageWidthException,
                                 InvalidReceiverException,
                                 InvalidSenderException)


class MessagesQueryValidation(QueryValidation):
    """
    This class is responsible for
    validating that a query is correct.
    """

    RECEIVER_ID = "recipient_id"
    SENDER_ID = "sender_id"
    MESSAGES = "messages"
    CONTENT = "content"
    TYPE = "type"
    URL = "url"
    TEXT = "text"
    SOURCE = "source"
    WIDTH = "width"
    HEIGHT = "height"


class SearchMessagesQueryValidation(MessagesQueryValidation,
                                    PaginationQueryValidation):
    """
    This class is responsible for
    validating that a query is correct.
    """

    @classmethod
    def validate(cls, query: dict) -> None:
        """
        This function validates that the
        query is valid to search for messages.
        NOTE: The query is passed by reference.
        """
        MessagesQueryValidation.validate(query)
        PaginationQueryValidation.validate(query)
        if not query.get(cls.RECEIVER_ID) or\
           not isinstance(query[cls.RECEIVER_ID], str):
            raise InvalidReceiverException()
        if not query.get(cls.SENDER_ID) or\
           not isinstance(query[cls.SENDER_ID], str):
            raise InvalidSenderException()


class SendMessageQueryValidation(MessagesQueryValidation):
    """
    This class is responsible for
    validating that a query is correct.
    """

    @classmethod
    def validate(cls, query: dict) -> None:
        """
        This function validates that the
        query is valid to send a new message.
        NOTE: The query is passed by reference.
        """
        MessagesQueryValidation.validate(query)
        if not query.get(cls.RECEIVER_ID) or\
           not isinstance(query[cls.RECEIVER_ID], str):
            raise InvalidReceiverException()
        if not query.get(cls.SENDER_ID) or\
           not isinstance(query[cls.SENDER_ID], str):
            raise InvalidSenderException()
        if query.get(cls.CONTENT) and\
           not isinstance(query[cls.CONTENT], dict):
            raise InvalidContentException()
        try:
            Type(query[cls.CONTENT].get(cls.TYPE))
        except ValueError:
            raise InvalidMessageTypeException()


class SendImageMessageQueryValidation(MessagesQueryValidation):
    """
    This class is responsible for
    validating that a query is correct.
    """

    @classmethod
    def validate(cls, query: dict) -> None:
        """
        This function validates that the
        query is valid to send a new image message.
        NOTE: The query is passed by reference.
        """
        if not query.get(cls.URL) or\
           not isinstance(query[cls.URL], str):
            raise InvalidMessageURLException()
        if not query.get(cls.WIDTH) or\
           not isinstance(query[cls.WIDTH], int)\
           or query[cls.WIDTH] < 0:
            raise InvalidMessageWidthException()
        if not query.get(cls.HEIGHT) or\
           not isinstance(query[cls.HEIGHT], int)\
           or query[cls.HEIGHT] < 0:
            raise InvalidMessageHeightException()


class SendTextMessageQueryValidation(MessagesQueryValidation):
    """
    This class is responsible for
    validating that a query is correct.
    """

    @classmethod
    def validate(cls, query: dict) -> None:
        """
        This function validates that the
        query is valid to send a new text message.
        NOTE: The query is passed by reference.
        """
        if not query.get(cls.TEXT) or\
           not isinstance(query[cls.TEXT], str):
            raise InvalidMessageTextException()


class SendVideoMessageQueryValidation(MessagesQueryValidation):
    """
    This class is responsible for
    validating that a query is correct.
    """

    @classmethod
    def validate(cls, query: dict) -> None:
        """
        This function validates that the
        query is valid to send a new video message.
        NOTE: The query is passed by reference.
        """
        if not query.get(cls.URL) or\
           not isinstance(query[cls.URL], str):
            raise InvalidMessageURLException()
        try:
            Source(query.get(cls.SOURCE))
        except ValueError:
            raise InvalidMessageSourceException()
