"""
Application API.

These classes are only responsible for authenticating
the request and handling exceptions on behalf of the client.
"""

import logging

from flask import request
from flask_restful import Resource
from flask_jwt_extended import jwt_required, get_jwt_identity

from app.controllers.users import UsersController
from app.exceptions import IguazuException
from app.worker.tasks import AsyncCreateUserTask

logger = logging.getLogger(__name__)


class UsersResource(Resource):
    """
    Users endpoint.
    """

    JOB_ID = "job_id"
    USERS = "users"

    @jwt_required
    def get(self) -> dict:
        """
        List users.
        """
        try:
            users = UsersController.search(request.json, get_jwt_identity())
        except IguazuException as error:
            logger.exception("Listing users | sf_error=%s", error)
            return error.to_json()
        else:
            return {
                self.USERS: [
                    user.to_json()
                    for user in users
                ]
            }

    @jwt_required
    def post(self) -> dict:
        """
        Create user.

        The async backend can be easily switched between
        UsersController.create() and UsersController.async_create()
        """
        try:
            response = AsyncCreateUserTask.delay(request.json, get_jwt_identity())
        except IguazuException as error:
            logger.exception("Create user | sf_error=%s", error)
            return error.to_json()
        else:
            return {
                self.JOB_ID: response.id,
            }
