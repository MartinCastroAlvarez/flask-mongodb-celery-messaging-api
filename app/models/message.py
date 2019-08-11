"""
Application models.

This classes are responsible for interacting
with the database. No authentication or business
logic is performed here.
"""

# pylint: disable=arguments-differ

import enum
import datetime

from app.models import mongo


class Type(enum.Enum):
    """
    Types Enum.
    """
    TEXT = "text"
    IMAGE = "image"
    VIDEO = "video"


class Source(enum.Enum):
    """
    Video Source Enum.
    """
    VIMEO = "vimeo"
    YOUTUBE = "youtube"


class Message(mongo.Document):
    """
    Message model.
    """

    sender_id = mongo.StringField(required=True, null=False)
    receiver_id = mongo.StringField(required=True, null=False)
    created_at = mongo.DateTimeField(default=datetime.datetime.utcnow)
    message_type = mongo.StringField(choices=[x.value for x in Type])
    source = mongo.StringField(choices=[x.value for x in Source])
    url = mongo.URLField()
    height = mongo.IntField()
    width = mongo.IntField()
    text = mongo.StringField(null=False)

    ID = "id"
    SENDER = "sender"
    RECEIVER = "recipient"
    TIMESTAMP = "timestamp"
    CONTENT = "content"
    TYPE = "type"
    TEXT = "text"
    USER = "url"
    SOURCE = "source"
    URL = "url"
    WIDTH = "width"
    HEIGHT = "height"

    meta = {
        'indexes': [{
            'fields': [
                '+created_at'  # Sorting key.
            ]
        }]
    }

    def __str__(self) -> str:
        """
        String serializer.
        """
        return "<Message: '{}'>".format(self.pk)

    def get_id(self) -> str:
        """
        Instance ID getter.
        """
        return str(self.pk)

    def to_json(self) -> dict:
        """
        JSON serializer.
        """
        content = {
            self.TYPE: self.message_type,
            self.TEXT: self.text,
            self.URL: self.url,
            self.SOURCE: self.source,
            self.WIDTH: self.width,
            self.HEIGHT: self.height,
        }
        content = {
            k: v
            for k, v in content.items()
            if v is not None
        }
        return {
            self.ID: self.get_id(),
            self.SENDER: self.sender_id,
            self.RECEIVER: self.receiver_id,
            self.TIMESTAMP: str(self.created_at),
            self.CONTENT: content,
        }
