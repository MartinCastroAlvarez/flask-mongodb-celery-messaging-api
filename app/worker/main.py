"""
Main worker CLI.
Run this script when executing the worker.
"""

# pylint: disable=invalid-name
# pylint: disable=unused-import

from app import create_app
from app.worker import celery, tasks  # noqa

create_app()
