"""
Async Workers

The libraries in this directory are responsible
for performing offline tasks, which don't require
the user to be waiting for.
"""

# pylint: disable=invalid-name

from celery import Celery

from app import config

celery = Celery(config.APP_NAME,
                backend=config.CELERY_RESULT_BACKEND,
                broker=config.CELERY_BROKER_URL)
