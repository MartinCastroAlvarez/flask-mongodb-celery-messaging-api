"""
Async Workers

The libraries in this directory are responsible
for performing offline tasks, which don't require
the user to be waiting for.
"""

import logging

from app.worker import celery

from app.exceptions import IguazuException
from app.controllers.users import UsersController
from app.controllers.notifications import NotificationsController

logger = logging.getLogger(__name__)


class AsyncCreateUserTask(celery.Task):
    """
    Create User async worker.
    """

    TITLE = "User Creation"
    CODE = 10099

    def run(self, query: dict, session: dict) -> None:
        """
        Create user asynchornously.
        """
        logger.debug("Worker | Create User | sf_query=%s", query)
        try:
            user = UsersController.create(query, session)
        except IguazuException as error:
            logger.exception("Worker | Create User | sf_error=%s", error)
            NotificationsController.send_me({
                NotificationsController.TITLE: self.TITLE,
                NotificationsController.CODE: self.CODE,
                NotificationsController.IS_ERROR: True,
                NotificationsController.MESSAGE: error.to_json()
            }, session)
        else:
            logger.debug("Worker | Create User | sf_user=%s", user)
            NotificationsController.send_me({
                NotificationsController.TITLE: self.TITLE,
                NotificationsController.CODE: self.CODE,
                NotificationsController.IS_ERROR: False,
                NotificationsController.MESSAGE: user.to_json()
            }, session)
