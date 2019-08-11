"""
Application models.

This classes are responsible for interacting
with the database. No authentication or business
logic is performed here.
"""

# pylint: disable=arguments-differ

import datetime

from app.models import mongo
from app.models.notification import Notification


class User(mongo.Document):
    """
    User model.
    """

    username = mongo.StringField(required=True, null=False, unique=True)
    password = mongo.StringField(required=True, null=False)
    created_at = mongo.DateTimeField(default=datetime.datetime.utcnow)
    notifications = mongo.EmbeddedDocumentListField(Notification)

    ID = "id"
    TIMESTAMP = "timestamp"
    USERNAME = "username"
    PASSWORD = "password"

    meta = {
        'indexes': [{
            'fields': [
                '+created_at'  # Sorting key.
            ]
        }, {
            'fields': [
                '#username'  # Hash access key.
            ]
        }]
    }

    def __str__(self) -> str:
        """
        String serializer.
        """
        return "<User: '{}'>".format(self.pk)

    def get_id(self) -> str:
        """
        Instance ID getter.
        """
        return str(self.pk)

    def to_json(self) -> dict:
        """
        JSON serializer.
        """
        return {
            self.ID: self.get_id(),
            self.TIMESTAMP: str(self.created_at),
            self.USERNAME: self.username,
            self.PASSWORD: self.password,
        }
