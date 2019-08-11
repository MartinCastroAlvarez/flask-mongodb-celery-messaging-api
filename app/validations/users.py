"""
App validations

The libraries in this directory are responsible
for validating queries and raising the proper exceptions.
"""

from app.validations import QueryValidation
from app.validations.pagination import PaginationQueryValidation

from app.exceptions.form import (InvalidPasswordException,
                                 InvalidUsernameException)


class UsersQueryValidation(QueryValidation):
    """
    This class is responsible for
    validating that a query is correct.
    """

    USERNAME = "username"
    PASSWORD = "password"


class SearchUsersQueryValidation(UsersQueryValidation,
                                 PaginationQueryValidation):
    """
    This class is responsible for
    validating that a query is correct.
    """

    @classmethod
    def validate(cls, query: dict) -> None:
        """
        This function validates that the
        query is valid to search for users.
        NOTE: The query is passed by reference.
        """
        UsersQueryValidation.validate(query)
        PaginationQueryValidation.validate(query)


class CreateUserQueryValidation(UsersQueryValidation):
    """
    This class is responsible for
    validating that a query is correct.
    """

    @classmethod
    def validate(cls, query: dict) -> None:
        """
        This function validates that the
        query is valid to create a new user.
        NOTE: The query is passed by reference.
        """
        UsersQueryValidation.validate(query)
        if not query.get(cls.USERNAME) or\
           not isinstance(query[cls.USERNAME], str):
            raise InvalidUsernameException()
        if not query.get(cls.PASSWORD) or\
           not isinstance(query[cls.PASSWORD], str):
            raise InvalidPasswordException()


class LoginQueryValidation(UsersQueryValidation):
    """
    This class is responsible for
    validating that a query is correct.
    """

    @classmethod
    def validate(cls, query: dict) -> None:
        """
        This function validates that the
        query is valid to do the login
        NOTE: The query is passed by reference.
        """
        UsersQueryValidation.validate(query)
        if not query.get(cls.USERNAME) or\
           not isinstance(query[cls.USERNAME], str):
            raise InvalidUsernameException()
        if not query.get(cls.PASSWORD) or\
           not isinstance(query[cls.PASSWORD], str):
            raise InvalidPasswordException()
