"""
Unit Tests.
"""

import unittest
from nose.plugins.attrib import attr
from unittest.mock import patch, MagicMock

from tests.api import TestPrivateApi
from app import exceptions, models


class TestMessagesApi(TestPrivateApi):
    """
    Testing messages endpoint.
    """

    @attr(unit_test=True)
    @patch('app.controllers.messages.MessagesController.search')
    def test_get_ok(self, controller):
        """
        Testing listing messages.
        """
        message1 = models.message.Message()
        message1.user_id = "user-1"
        message1.text = "text-1"
        message1.url = "url-1"
        message2 = models.message.Message()
        message2.user_id = "user-1"
        message2.text = "text-1"
        message2.url = "url-1"
        controller.return_value = (message1, message2)
        response = self.client.get("/messages", headers=self.headers).get_json()
        self.assertEqual(response['messages'][0], message1.to_json())
        self.assertEqual(response['messages'][1], message2.to_json())

    @attr(unit_test=True)
    @patch('app.controllers.messages.MessagesController.search')
    def test_get_error(self, controller):
        """
        Testing listing messages and getting an error.
        """
        error = exceptions.auth.IguazuException()
        controller.side_effect = error
        response = self.client.get("/messages", headers=self.headers).get_json()
        self.assertEqual(response, error.to_json())

    @attr(unit_test=True)
    @patch('app.worker.tasks.AsyncSendMessageTask.delay')
    def test_post_async(self, task):
        """
        Testing sending a message asynchronously.
        """
        task.return_value = MagicMock(id="912093091")
        response = self.client.post("/messages", headers=self.headers).get_json()
        self.assertEqual(response["job_id"], "912093091")
