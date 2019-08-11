"""
Async Workers

The libraries in this directory are responsible
for performing offline tasks, which don't require
the user to be waiting for.
"""

# pylint: disable=invalid-name
# pylint: disable=unused-import

from app.main import create_app
from app.worker import celery  # noqa
import app.worker.tasks  # noqa

create_app()
