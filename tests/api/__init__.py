"""
Unit Tests.
"""

import unittest
from unittest.mock import patch

from flask_jwt_extended import create_access_token
from app import create_app, config


class TestPublicApi(unittest.TestCase):
    """
    Public API resources tests.
    """

    @patch('app.mongo.init_app')
    @patch('app.redis.init_app')
    def setUp(self, redis, mongo):
        """
        Executed prior to each test.
        """
        self.app = create_app()
        self.client = self.app.test_client()
        mongo.assert_called_once()
        redis.assert_called_once()


class TestPrivateApi(TestPublicApi):
    """
    Private API resources tests.
    """

    def setUp(self):
        """
        Executed prior to each test.
        """
        TestPublicApi.setUp(self)
        with self.app.app_context():
            self.token = create_access_token(identity={})
            self.headers = {
                config.TOKEN_HEADER: "Bearer {}".format(self.token)
            }
