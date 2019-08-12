"""
Unit Tests.
"""

from nose.plugins.attrib import attr
from unittest.mock import patch, MagicMock

from tests.api import TestPrivateApi
from app import exceptions, models


class TestUsersApi(TestPrivateApi):
    """
    Testing users endpoint.
    """

    @attr(unit_test=True)
    @patch('app.controllers.users.UsersController.search')
    def test_get_ok(self, controller):
        """
        Testing listing users.
        """
        user1 = models.user.User()
        user1.username = "user-1"
        user1.password = "pass-1"
        user2 = models.user.User()
        user2.username = "user-2"
        user2.password = "pass-2"
        controller.return_value = (user1, user2)
        response = self.client.get("/users", headers=self.headers).get_json()
        self.assertEqual(response['users'][0], user1.to_json())
        self.assertEqual(response['users'][1], user2.to_json())
        controller.assert_called_once()

    @attr(unit_test=True)
    @patch('app.controllers.users.UsersController.search')
    def test_get_error(self, controller):
        """
        Testing listing users and getting an error.
        """
        error = exceptions.auth.IguazuException()
        controller.side_effect = error
        response = self.client.get("/users", headers=self.headers).get_json()
        self.assertEqual(response, error.to_json())
        controller.assert_called_once()

    @attr(unit_test=True)
    @patch('app.worker.tasks.AsyncCreateUserTask.delay')
    def test_post_async(self, task):
        """
        Testing creating an User asynchronously.
        """
        task.return_value = MagicMock(id="1892398182")
        response = self.client.post("/users", headers=self.headers).get_json()
        self.assertEqual(response["job_id"], "1892398182")
        task.assert_called_once()
