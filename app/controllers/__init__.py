"""
Application controller.

These functions are responsible for validating
the request and interacting with the model.

These functions are also responsible for deciding
from which storage engine to read from.
"""

# pylint: disable=invalid-name

import json
import pickle
import base64

from flask_redis import FlaskRedis
from app import config

redis = FlaskRedis()


class Cache:
    """
    Cached dict entity.
    """

    def __init__(self, key: str) -> None:
        """
        Constructing cache.
        """
        self.key = key

    def __str__(self) -> str:
        """
        String serializer.
        """
        return "<Cache: '{}'>.".format(self.key)

    def get_value(self) -> object:
        """
        Cached value getter.
        """
        value = redis.get(self.key)
        value = base64.b64decode(value)
        return pickle.loads(value)

    def set_value(self, value: object, expires_in: int = 10) -> None:
        """
        Cached value setter.
        """
        value = base64.b64encode(pickle.dumps(value, 0))
        redis.set(self.key, value.decode(config.ENCODING), expires_in)

    def is_cached(self) -> bool:
        """
        Returns True if value is cached.
        """
        return redis.exists(self.key) > 0


class Queue(Cache):
    """
    Cached queue entity.
    """

    def __str__(self) -> str:
        """
        String serializer.
        """
        return "<Queue: '{}'>.".format(self.key)

    def get_values(self, start: int, end: int) -> list:
        """
        Cached value getter.
        """
        return [
            json.loads(base64.b64decode(v).decode(config.ENCODING))
            for v in redis.lrange(self.key, start, end)
        ]

    def add(self, value: dict) -> None:
        """
        Cached value setter.
        """
        new_value = base64.b64encode(json.dumps(value).encode(config.ENCODING))
        redis.lpush(self.key, new_value)
