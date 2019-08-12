"""
Unit Tests.
"""

from nose.plugins.attrib import attr
from unittest.mock import patch

from tests.api import TestPublicApi
from app import exceptions


class TestHealthApi(TestPublicApi):
    """
    Testing health endpoint.
    """

    @attr(unit_test=True)
    @patch('app.controllers.health.HealthController.check')
    def test_post_ok(self, controller):
        """
        Testing the health endpoint when the app is OK.
        """
        controller.return_value = {"status": "ok"}
        response = self.client.post("/health").get_json()
        self.assertEqual(response, controller.return_value)
        controller.assert_called_once()

    @attr(unit_test=True)
    @patch('app.controllers.health.HealthController.check')
    def test_post_error(self, controller):
        """
        Testing the health endpoint when the app is unhealthy.
        """
        error = exceptions.health.DatabaseHealthException()
        controller.side_effect = error
        response = self.client.post("/health").get_json()
        self.assertEqual(response, error.to_json())
        controller.assert_called_once()
