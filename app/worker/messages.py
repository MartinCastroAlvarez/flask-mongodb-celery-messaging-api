"""
Async Workers

The libraries in this directory are responsible
for performing offline tasks, which don't require
the user to be waiting for.
"""

import logging

from app.worker import celery

from app.exceptions import IguazuException
from app.controllers.messages import MessagesController
from app.controllers.notifications import NotificationsController

logger = logging.getLogger(__name__)


class AsyncSendMessageTask(celery.Task):
    """
    Send async message worker.
    """

    TITLE = "New Message"
    CODE = 10095

    def run(self, query: dict, session: dict) -> None:
        """
        Send message asynchornously.
        """
        logger.debug("Worker | Send Message | sf_query=%s", query)
        try:
            message = MessagesController.send(query, session)
        except IguazuException as error:
            logger.exception("Worker | Send Message | sf_error=%s", error)
            NotificationsController.send_me({
                NotificationsController.TITLE: self.TITLE,
                NotificationsController.CODE: self.CODE,
                NotificationsController.IS_ERROR: True,
                NotificationsController.MESSAGE: error.to_json()
            }, session)
        else:
            logger.debug("Worker | Send Message | sf_message=%s", message)
            NotificationsController.send_me({
                NotificationsController.TITLE: self.TITLE,
                NotificationsController.CODE: self.CODE,
                NotificationsController.IS_ERROR: False,
                NotificationsController.MESSAGE: message.to_json()
            }, session)
