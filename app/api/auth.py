"""
Application API.

These classes are only responsible for authenticating
the request and handling exceptions on behalf of the client.
"""

import logging

from flask import request
from flask_restful import Resource

from app.controllers.users import UsersController
from app.exceptions import IguazuException

logger = logging.getLogger(__name__)


class AuthResource(Resource):
    """
    Authentication endpoint.
    """

    ACCESS_TOKEN = "token"
    REFRESH_TOKEN = "refresh_token"

    def post(self) -> dict:
        """
        Do login.
        """
        try:
            user, token, refresh = UsersController.login(request.json)
        except IguazuException as error:
            logger.exception("Do login | sf_error=%s", error)
            return error.to_json()
        else:
            response = user.to_json()
            response[self.ACCESS_TOKEN] = token
            response[self.REFRESH_TOKEN] = refresh
            return response
