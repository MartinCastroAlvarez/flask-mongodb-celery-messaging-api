"""
Application controller.

These functions are responsible for validating
the request and interacting with the model.

These functions are also responsible for deciding
from which storage engine to read from.
"""

import typing

from app import config
from app.controllers import Cache
from app.models.user import User
from app.security.encryption import Hash
from app.security.login import Session
from app.validations.users import (CreateUserQueryValidation,
                                   SearchUsersQueryValidation,
                                   LoginQueryValidation)

from app.exceptions.auth import (WrongPasswordException,
                                 UsernameAlreadyTakenException)
from app.exceptions.not_found import UserNotFoundException
from app.exceptions.form import (InvalidIdentifierException,
                                 InvalidUsernameException)


class UsersController:
    """
    User business logic.

    @method login(): Authenticate username and password.
    @method create(): Create new user.
    @method get_by_id(): Search for one user by ID.
    @method get_by_username(): Search for one user by username.
    """

    LIMIT = "limit"
    USERNAME = "username"
    PASSWORD = "password"

    @classmethod
    def login(cls, query: dict) -> typing.Tuple:
        """
        Business method to do login.
        """
        LoginQueryValidation.validate(query)
        user = cls.get_by_username(query[cls.USERNAME])
        if not Hash.match(user.password, query[cls.PASSWORD]):
            raise WrongPasswordException()
        cache = Cache(f"token-{user.username}")
        if cache.is_cached():
            access_token, refresh_token = cache.get_value()  # type: ignore
        else:
            access_token, refresh_token = Session.get_token(user)
            cache.set_value([access_token, refresh_token])
        return user, access_token, refresh_token

    @classmethod
    def create(cls, query: dict, session: dict) -> User:
        """
        Business method to create an user.
        """
        assert isinstance(session, dict)
        CreateUserQueryValidation.validate(query)
        try:
            cls.get_by_username(query[cls.USERNAME])
        except UserNotFoundException:
            new_user = User()
            new_user.username = query[cls.USERNAME]
            new_user.password = Hash.obfuscate(query[cls.PASSWORD])
            new_user.save()
        else:
            raise UsernameAlreadyTakenException()
        return new_user

    @classmethod
    def get_by_username(cls, username: str) -> User:
        """
        Business method to get user by username.

        If the user is cached, it will be read from cache.
        Otherwise, it will be read from the database and,
        if it exists, it will be cached.
        """
        if not username or not isinstance(username, str):
            raise InvalidUsernameException()
        cache = Cache(f"user-{username}")
        if cache.is_cached():
            return cache.get_value()  # type: ignore
        users = User.objects(username=username)
        if not users:
            raise UserNotFoundException()
        cache.set_value(users[0], expires_in=config.CACHE_USER)
        return users[0]

    @classmethod
    def get_by_id(cls, user_id: str) -> User:
        """
        Business method to get user by ID.

        If the user is cached, it will be read from cache.
        Otherwise, it will be read from the database and,
        if it exists, it will be cached.
        """
        if not user_id or not isinstance(user_id, str):
            raise InvalidIdentifierException()
        cache = Cache(f"user-{user_id}")
        if cache.is_cached():
            return cache.get_value()  # type: ignore
        users = User.objects(pk=user_id)
        if not users:
            raise UserNotFoundException()
        cache.set_value(users[0], expires_in=config.CACHE_USER)
        return users[0]

    @classmethod
    def search(cls, query: dict, session: dict) -> typing.List[User]:
        """
        Business method to list users.
        """
        assert isinstance(session, dict)
        SearchUsersQueryValidation.validate(query)
        return list(User.objects.limit(query[cls.LIMIT]))
