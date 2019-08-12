"""
Main Flask app.

This file is required by the Docker image:
https://github.com/tiangolo/uwsgi-nginx-flask-docker
"""

import logging

from flask import Flask

from app import config
from app.api import api
from app.security.login import jwt

from app.controllers.users import UsersController
from app.exceptions.auth import UsernameAlreadyTakenException

from app.controllers import redis
from app.worker import celery
from app.models import mongo

logger = logging.getLogger(__name__)


def create_app() -> Flask:  # pylint: disable=too-many-statements
    """
    Flask Factory pattern.

    Reference:
    http://flask.pocoo.org/docs/1.0/patterns/appfactories/
    """
    iguazu = Flask(__name__)
    iguazu.url_map.strict_slashes = False

    # Secret Key is required by Flask-Session.
    iguazu.secret_key = config.SECRET

    # Setting debug mode.
    iguazu.debug = bool(config.DEBUG)

    # Updating logger messages.
    logging.basicConfig(level=config.LOG_LEVEL, format=config.LOG_FORMAT)

    # Loading DB connector.
    iguazu.config['MONGODB_DB'] = config.MONGO_NAME
    iguazu.config['MONGODB_HOST'] = config.MONGO_HOST
    iguazu.config['MONGODB_PORT'] = config.MONGO_PORT
    iguazu.config['MONGODB_USERNAME'] = config.MONGO_USER
    iguazu.config['MONGODB_PASSWORD'] = config.MONGO_PASS
    mongo.init_app(iguazu)

    # Loading login handler.
    iguazu.config["JWT_SECRET_KEY"] = config.SECRET
    iguazu.config["JWT_HEADER_NAME"] = config.JWT_HEADER_NAME
    jwt.init_app(iguazu)

    # Loading celery config.
    celery.conf.update(iguazu.config)
    iguazu.config["CELERY_RESULT_BACKEND"] = config.CELERY_RESULT_BACKEND
    iguazu.config["CELERY_BROKER_URL"] = config.CELERY_BROKER_URL

    def call(self, *args, **kwargs):
        """
        Main call.
        """
        with iguazu.app_context():
            return self.run(*args, **kwargs)

    celery.Task.__call__ = call

    # Loading cache connector.
    iguazu.config["REDIS_URL"] = config.REDIS_URI
    redis.init_app(iguazu)

    # Creating an admin.
    # WARNING: This piece of code has been created for the demo.
    #          This user will be used for testing purposes.
    if config.ADMIN_USER and config.ADMIN_PASS:
        with iguazu.app_context():
            logger.warning("Setting admin password.")
            try:
                admin = UsersController.create({
                    UsersController.USERNAME: config.ADMIN_USER,
                    UsersController.PASSWORD: config.ADMIN_PASS,
                }, {})
            except UsernameAlreadyTakenException:
                logger.warning("Admin already exists!")
            else:
                logger.warning("Admin created! | sf_admin=%s", admin)

    # Registering app views.
    api.init_app(iguazu)

    # End of app factory.
    logger.info("App started!")
    return iguazu
