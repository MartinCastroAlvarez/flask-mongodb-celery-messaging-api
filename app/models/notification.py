"""
Application models.

This classes are responsible for interacting
with the database. No authentication or business
logic is performed here.
"""

# pylint: disable=arguments-differ

import datetime

from app.models import mongo


class Notification(mongo.EmbeddedDocument):
    """
    Notification model.
    """

    created_at = mongo.DateTimeField(default=datetime.datetime.utcnow)
    title = mongo.StringField(required=True, null=False)
    message = mongo.DictField(required=True)
    code = mongo.IntField(required=True)
    is_error = mongo.BooleanField(required=True, default=False)

    CODE = "code"
    IS_ERROR = "is_error"
    TIMESTAMP = "timestamp"
    TITLE = "title"
    MESSAGE = "message"

    def __str__(self) -> str:
        """
        String serializer.
        """
        return "<Notification: '{}'>".format(self.title)

    def to_json(self) -> dict:
        """
        JSON serializer.
        """
        return {
            self.MESSAGE: self.message,
            self.IS_ERROR: self.is_error,
            self.CODE: self.code,
            self.TITLE: self.title,
            self.TIMESTAMP: str(self.created_at),
        }
