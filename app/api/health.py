"""
Application API.

These classes are only responsible for authenticating
the request and handling exceptions on behalf of the client.
"""

import logging

from flask_restful import Resource

from app.controllers.health import HealthController
from app.exceptions import IguazuException

logger = logging.getLogger(__name__)


class HealthResource(Resource):
    """
    Health endpoint.
    """

    def get(self) -> dict:
        """
        GET app health.
        """
        try:
            status = HealthController.check()
        except IguazuException as error:
            logger.exception("Get health | sf_error=%s", error)
            return error.to_json()
        else:
            return status

    def post(self) -> dict:
        """
        GET app health.
        """
        return self.get()
