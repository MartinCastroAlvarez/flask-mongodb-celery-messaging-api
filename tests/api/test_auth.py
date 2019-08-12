"""
Unit Tests.
"""

import unittest
from nose.plugins.attrib import attr
from unittest.mock import patch

from tests.api import TestPublicApi
from app import exceptions, models


class TestAuthApi(TestPublicApi):
    """
    Testing auth endpoint.
    """

    @attr(unit_test=True)
    @patch('app.controllers.users.UsersController.login')
    def test_post_ok(self, controller):
        """
        Testing a successful login.
        """
        user = models.user.User()
        user.username = "my-username"
        user.password = "lorem-ipsum"
        controller.return_value = user, "access-token", "refresh-token"
        response = self.client.post("/login").get_data(as_text=True)
        self.assertIn("access-token", response)
        self.assertIn("refresh-token", response)
        self.assertIn(user.username, response)
        self.assertIn(user.password, response)

    @attr(unit_test=True)
    @patch('app.controllers.users.UsersController.login')
    def test_post_error(self, controller):
        """
        Testing an unsuccessful login.
        """
        error = exceptions.auth.WrongPasswordException()
        controller.side_effect = error
        response = self.client.post("/login").get_json()
        self.assertEqual(response, error.to_json())
