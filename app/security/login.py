"""
Security libraries.

These classes are responsible for ensuring
a certain degree of security in the app.
"""

# pylint: disable=invalid-name

import typing
import logging

from flask_jwt_extended import (JWTManager,
                                create_access_token,
                                create_refresh_token)

from app.models.user import User

logger = logging.getLogger(__name__)


class Session:
    """
    JWT Token entity.
    """

    ID = "id"
    USERNAME = "username"

    @classmethod
    def get_token(cls, user: User) -> typing.Tuple[str, str]:
        """
        Public method to generate a new access and refresh token.
        """
        logger.debug("Generating Access Token | sf_user=%s", user)
        session = {
            cls.ID: user.get_id(),
            cls.USERNAME: user.username,
        }
        logger.debug("Generating Access Token | sf_session=%s", session)
        access_token = create_access_token(identity=session)
        refresh_token = create_refresh_token(identity=session)
        return access_token, refresh_token


jwt = JWTManager()
