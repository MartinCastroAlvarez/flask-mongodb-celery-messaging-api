"""
App validations

The libraries in this directory are responsible
for validating queries and raising the proper exceptions.
"""

from app.validations import QueryValidation
from app.validations.pagination import PaginationQueryValidation

from app.exceptions.form import (InvalidUserIdentifierException,
                                 InvalidMessageException,
                                 InvalidTitleException,
                                 InvalidCodeException)


class NotificationsQueryValidation(QueryValidation):
    """
    This class is responsible for
    validating that a query is correct.
    """

    USER_ID = "user_id"

    TITLE = "title"
    CODE = "code"
    IS_ERROR = "is_error"
    MESSAGE = "message"


class SearchNotificationsQueryValidation(NotificationsQueryValidation,
                                         PaginationQueryValidation):
    """
    This class is responsible for
    validating that a query is correct.
    """

    @classmethod
    def validate(cls, query: dict) -> None:
        """
        This function validates that the
        query is valid to search for notifications.
        NOTE: The query is passed by reference.
        """
        NotificationsQueryValidation.validate(query)
        PaginationQueryValidation.validate(query)
        if not query.get(cls.USER_ID) or\
           not isinstance(query[cls.USER_ID], str):
            raise InvalidUserIdentifierException()


class SendNotificationQueryValidation(NotificationsQueryValidation):
    """
    This class is responsible for
    validating that a query is correct.
    """

    @classmethod
    def validate(cls, query: dict) -> None:
        """
        This function validates that the
        query is valid to send a new notification.
        NOTE: The query is passed by reference.
        """
        NotificationsQueryValidation.validate(query)
        if not query.get(cls.MESSAGE) or\
           not isinstance(query[cls.MESSAGE], dict):
            raise InvalidMessageException()
        if not query.get(cls.TITLE) or\
           not isinstance(query[cls.TITLE], str):
            raise InvalidTitleException()
        if not query.get(cls.CODE) or\
           not isinstance(query[cls.CODE], int):
            raise InvalidCodeException()
        if not query.get(cls.USER_ID) or\
           not isinstance(query[cls.USER_ID], str):
            raise InvalidUserIdentifierException()
