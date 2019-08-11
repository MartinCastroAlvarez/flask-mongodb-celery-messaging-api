"""
Application API.

These classes are only responsible for authenticating
the request and handling exceptions on behalf of the client.
"""

# pylint: disable=invalid-name

from flask_restful import Api

from app.api.health import HealthResource
from app.api.users import UsersResource
from app.api.notifications import NotificationsResource
from app.api.messages import MessagesResource
from app.api.auth import AuthResource

api = Api()
api.add_resource(AuthResource, "/v1/auth", "/v1/login", "/login", "/auth")
api.add_resource(UsersResource, "/v1/users", "/users")
api.add_resource(MessagesResource, "/v1/messages", "/messages")
api.add_resource(HealthResource, "/", "/v1/health", "/v1/check", "/health", "/check")
api.add_resource(NotificationsResource, "/v1/notifications", "/notifications")
