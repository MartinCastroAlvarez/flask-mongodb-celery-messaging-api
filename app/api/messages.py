"""
Application API.

These classes are only responsible for authenticating
the request and handling exceptions on behalf of the client.
"""

import logging

from flask import request
from flask_restful import Resource
from flask_jwt_extended import jwt_required, get_jwt_identity

from app.controllers.messages import MessagesController
from app.worker.tasks import AsyncSendMessageTask
from app.exceptions import IguazuException

logger = logging.getLogger(__name__)


class MessagesResource(Resource):
    """
    Messages endpoint.
    """

    JOB_ID = "job_id"
    MESSAGES = "messages"

    @jwt_required
    def get(self) -> dict:
        """
        List messages.
        """
        try:
            messages = MessagesController.search(request.json, get_jwt_identity())
        except IguazuException as error:
            logger.exception("List messages | sf_error=%s", error)
            return error.to_json()
        else:
            return {
                self.MESSAGES: [
                    message.to_json()
                    for message in messages
                ]
            }

    @jwt_required
    def post(self) -> dict:
        """
        Send new message.
        """
        try:
            response = AsyncSendMessageTask.delay(request.json, get_jwt_identity())
        except IguazuException as error:
            logger.exception("Send Message | sf_error=%s", error)
            return error.to_json()
        else:
            return {
                self.JOB_ID: response.id,
            }
