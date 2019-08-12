"""
Application configuration.
"""

import os
import logging

DEBUG = os.environ.get("DEBUG", "")
SECRET = os.environ.get("SECRET", "default-secret-key")

ADMIN_USER = os.environ.get("ADMIN_USER", "")
ADMIN_PASS = os.environ.get("ADMIN_PASS", "")

CACHE_HOST = os.environ.get("CACHE_HOST", "")
CACHE_PORT = int(os.environ.get("CACHE_PORT", 6379))
CACHE_NAME = os.environ.get("CACHE_NAME", "")
CACHE_PASS = os.environ.get("CACHE_PASS", "")
REDIS_URI = "redis://:{}@{}:{}/{}".format(CACHE_PASS, CACHE_HOST,
                                          CACHE_PORT, CACHE_NAME)

CELERY_RESULT_BACKEND = "redis://:{}@{}:{}".format(CACHE_PASS,
                                                   CACHE_HOST,
                                                   CACHE_PORT)
CELERY_BROKER_URL = "redis://:{}@{}:{}".format(CACHE_PASS,
                                               CACHE_HOST,
                                               CACHE_PORT)

MONGO_HOST = os.environ.get("MONGO_HOST", "")
MONGO_PORT = int(os.environ.get("MONGO_PORT", 27017))
MONGO_NAME = os.environ.get("MONGO_NAME", "")
MONGO_USER = os.environ.get("MONGO_USER", "")
MONGO_PASS = os.environ.get("MONGO_PASS", "")

API_ROOT = os.path.dirname(os.path.abspath(__file__))
APP_ROOT = os.path.dirname(API_ROOT)
APP_NAME = os.path.basename(APP_ROOT)

LOG_FORMAT = "%(asctime)s [%(levelname)s] %(name)s: %(message)s"
LOG_LEVEL = logging.DEBUG if DEBUG else logging.INFO

JWT_HEADER_NAME = os.environ.get('JWT_HEADER_NAME', 'Authorization')
SALT = os.environ.get("SALT", "default-salt-key")
ENCODING = "utf-8"
TOKEN_HEADER = "Authorization"
PASSWORD_FIXED_COMPARISSON_TIME = (0, 3)
ENCRYPTION_ALGORITHM = "HS256"

CACHE_USER = 100
CACHE_TOKEN = 10

RUNSERVER_PORT = "8080"
RUNSERVER_HOST = "host"
RUNSERVER_DEBUG = True
