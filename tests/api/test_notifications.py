"""
Unit Tests.
"""

import unittest
from nose.plugins.attrib import attr
from unittest.mock import patch, MagicMock

from tests.api import TestPrivateApi
from app import exceptions


class TestNotificationsApi(TestPrivateApi):
    """
    Testing notifications endpoint.
    """

    @attr(unit_test=True)
    @patch('app.controllers.notifications.NotificationsController.search_mine')
    def test_get_ok(self, controller):
        """
        Testing listing notifications.
        """
        notification1 = dict(lorem=1, ipsum=2, dolor=3, sit=4, amet=5)
        notification2 = dict(lorem=1, ipsum=2, dolor=3, sit=4, amet=5)
        controller.return_value = (notification1, notification2)
        response = self.client.get("/notifications", headers=self.headers).get_json()
        self.assertEqual(response['notifications'][0], notification1)
        self.assertEqual(response['notifications'][1], notification2)
        controller.assert_called_once()

    @attr(unit_test=True)
    @patch('app.controllers.notifications.NotificationsController.search_mine')
    def test_get_error(self, controller):
        """
        Testing listing notifications and getting an error.
        """
        error = exceptions.auth.IguazuException()
        controller.side_effect = error
        response = self.client.get("/notifications", headers=self.headers).get_json()
        self.assertEqual(response, error.to_json())
        controller.assert_called_once()
