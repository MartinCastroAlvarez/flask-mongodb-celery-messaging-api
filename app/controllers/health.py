"""
Application controller.

These functions are responsible for validating
the request and interacting with the model.

These functions are also responsible for deciding
from which storage engine to read from.
"""

import logging

from app import config
from app.exceptions.health import (DatabaseHealthException,
                                   CacheHealthException)
from app.controllers.users import UsersController
from app.controllers import redis

logger = logging.getLogger(__name__)


class HealthController:
    """
    Health business logic.

    @method check(): Perform health check and get status.
    """

    HEALTH = "health"
    OK = "ok"

    @classmethod
    def check(cls) -> dict:
        """
        Business method to perform a health check.
        """
        cls.__check_db_health()
        cls.__check_cache_health()
        return {
            cls.HEALTH: cls.OK,
        }

    @classmethod
    def __check_db_health(cls) -> None:
        """
        Private business method to check the db connection.
        """
        query = {
            UsersController.LIMIT: 1,
        }
        try:
            UsersController.search(query, {})
        except:  # noqa
            logger.exception("DB is down!")
            raise DatabaseHealthException()

    @classmethod
    def __check_cache_health(cls) -> None:
        """
        Private business method to check the db connection.
        """
        try:
            redis.set("health-check", "lorem-ipsum")
            value = redis.get("health-check").decode(config.ENCODING)
            assert value == "lorem-ipsum", value
        except:  # noqa
            logger.exception("Cache is down!")
            raise CacheHealthException()
