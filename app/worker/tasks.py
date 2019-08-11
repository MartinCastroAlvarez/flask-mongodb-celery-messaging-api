"""
Async Workers

The libraries in this directory are responsible
for performing offline tasks, which don't require
the user to be waiting for.
"""

# pylint: disable=invalid-name

from app.worker import celery

from app.worker.users import AsyncCreateUserTask
from app.worker.messages import AsyncSendMessageTask

AsyncCreateUserTask = celery.register_task(AsyncCreateUserTask())  # type: ignore
AsyncSendMessageTask = celery.register_task(AsyncSendMessageTask())  # type: ignore
