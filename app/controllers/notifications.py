"""
Application controller.

These functions are responsible for validating
the request and interacting with the model.

These functions are also responsible for deciding
from which storage engine to read from.
"""

import typing

from app.models.user import User
from app.controllers import Queue
from app.security.login import Session
from app.models.notification import Notification
from app.validations.notifications import (SendNotificationQueryValidation,
                                           SearchNotificationsQueryValidation)


class NotificationsController:
    """
    Notifications business logic.

    @method search(): Search for messages.
    @method send(): Send a new message.
    """

    LIMIT = "limit"
    USER_ID = "user_id"

    TITLE = "title"
    CODE = "code"
    IS_ERROR = "is_error"
    MESSAGE = "message"

    @classmethod
    def search(cls, query: dict, session: dict) -> typing.List[dict]:
        """
        Business method to search user messages.
        """
        assert isinstance(session, dict)
        SearchNotificationsQueryValidation.validate(query)
        user_id = query[cls.USER_ID]
        queue = Queue(f"notifications-{user_id}")
        notifications = queue.get_values(start=0, end=query[cls.LIMIT] - 1)
        return notifications

    @classmethod
    def send(cls, query: dict, session: dict) -> Notification:
        """
        Business method to send a new notification.
        """
        assert isinstance(session, dict)
        SendNotificationQueryValidation.validate(query)
        user = User.objects.get(pk=query[cls.USER_ID])
        notification = Notification()
        notification.code = query[cls.CODE]
        notification.is_error = query.get(cls.IS_ERROR)
        notification.title = query[cls.TITLE]
        notification.message = query[cls.MESSAGE]
        user.notifications.append(notification)
        user.save()
        queue = Queue(f"notifications-{user.id}")
        queue.add(notification.to_json())
        return notification

    @classmethod
    def send_me(cls, query: dict, session: dict) -> Notification:
        """
        Business method to send a new notification to the current user.
        """
        query[cls.USER_ID] = session.get(Session.ID)
        return cls.send(query, session)

    @classmethod
    def search_mine(cls, query: dict, session: dict) -> typing.List[dict]:
        """
        Business method to search for my own notifications only.
        """
        query[cls.USER_ID] = session.get(Session.ID)
        return cls.search(query, session)
