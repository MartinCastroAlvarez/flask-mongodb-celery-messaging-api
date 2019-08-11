"""
Application controller.

These functions are responsible for validating
the request and interacting with the model.

These functions are also responsible for deciding
from which storage engine to read from.
"""

import typing

from app.models.message import Message, Type
from app.controllers.users import UsersController
from app.validations.messages import (SendMessageQueryValidation,
                                      SendVideoMessageQueryValidation,
                                      SendImageMessageQueryValidation,
                                      SendTextMessageQueryValidation,
                                      SearchMessagesQueryValidation)


class MessagesController:
    """
    Messages business logic.

    @method search(): Search for messages.
    @method send(): Send a new message.
    """

    START = "start"
    LIMIT = "limit"
    RECEIVER_ID = "recipient_id"
    SENDER_ID = "sender_id"
    MESSAGES = "messages"
    CONTENT = "content"
    TYPE = "type"
    URL = "url"
    TEXT = "text"
    SOURCE = "source"
    WIDTH = "width"
    HEIGHT = "height"

    @classmethod
    def search(cls, query: dict, session: dict) -> typing.List[Message]:
        """
        Business method to search user messages.
        """
        assert isinstance(session, dict)
        SearchMessagesQueryValidation.validate(query)
        search_query = {}
        search_query["sender_id"] = query[cls.SENDER_ID]
        search_query["receiver_id"] = query[cls.RECEIVER_ID]
        if query.get(cls.START):
            search_query['pk__lt'] = query[cls.START]
        messages = Message.objects(**search_query)
        messages = messages.order_by('-pk')
        messages = messages.limit(query[cls.LIMIT])
        return list(messages)

    @classmethod
    def send(cls, query: dict, session: dict) -> Message:
        """
        Business method to send a new message.
        """
        assert isinstance(session, dict)
        SendMessageQueryValidation.validate(query)
        receiver = UsersController.get_by_id(query[cls.RECEIVER_ID])
        sender = UsersController.get_by_id(query[cls.SENDER_ID])
        content = query[cls.CONTENT]
        func = {
            Type.VIDEO.value: cls.__send_video,
            Type.TEXT.value: cls.__send_text,
            Type.IMAGE.value: cls.__send_image,
        }[content[cls.TYPE]]
        message = func(content)
        message.message_type = content[cls.TYPE]
        message.sender_id = sender.get_id()
        message.receiver_id = receiver.get_id()
        message.save()
        return message

    @classmethod
    def __send_image(cls, content: dict) -> Message:
        """
        Business method to send an imagem message.
        """
        SendImageMessageQueryValidation.validate(content)
        new_message = Message()
        new_message.url = content[cls.URL]
        new_message.width = content[cls.WIDTH]
        new_message.height = content[cls.HEIGHT]
        return new_message

    @classmethod
    def __send_text(cls, content: dict) -> Message:
        """
        Business method to send a text message.
        """
        SendTextMessageQueryValidation.validate(content)
        new_message = Message()
        new_message.text = content[cls.TEXT]
        return new_message

    @classmethod
    def __send_video(cls, content: dict) -> Message:
        """
        Business method to send a video message.
        """
        SendVideoMessageQueryValidation.validate(content)
        new_message = Message()
        new_message.url = content[cls.URL]
        new_message.source = content[cls.SOURCE]
        return new_message
