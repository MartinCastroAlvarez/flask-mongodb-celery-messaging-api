"""
Application API.

These classes are only responsible for authenticating
the request and handling exceptions on behalf of the client.
"""

import logging

from flask import request
from flask_restful import Resource
from flask_jwt_extended import jwt_required, get_jwt_identity

from app.controllers.notifications import NotificationsController
from app.exceptions import IguazuException

logger = logging.getLogger(__name__)


class NotificationsResource(Resource):
    """
    Notifications endpoint.
    """

    NOTIFICATIONS = "notifications"

    @jwt_required
    def get(self) -> dict:
        """
        List notifications.
        """
        try:
            notifications = NotificationsController.search_mine(request.json,
                                                                get_jwt_identity())
        except IguazuException as error:
            logger.exception("List notifications | sf_error=%s", error)
            return error.to_json()
        else:
            return {
                self.NOTIFICATIONS: notifications,
            }
