"""
Main Flask app.

This file is required by the Docker image:
https://github.com/tiangolo/uwsgi-nginx-flask-docker
"""

# pylint: disable=too-many-statements

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


def create_app() -> Flask:
    """
    Flask Factory pattern.

    Reference:
    http://flask.pocoo.org/docs/1.0/patterns/appfactories/
    """
    app = Flask(__name__)  # pylint: disable=redefined-outer-name
    app.url_map.strict_slashes = False

    # Secret Key is required by Flask-Session.
    app.secret_key = config.SECRET

    # Setting debug mode.
    app.debug = bool(config.DEBUG)

    # Updating logger messages.
    logging.basicConfig(level=config.LOG_LEVEL, format=config.LOG_FORMAT)

    # Loading DB connector.
    app.config['MONGODB_DB'] = config.MONGO_NAME
    app.config['MONGODB_HOST'] = config.MONGO_HOST
    app.config['MONGODB_PORT'] = config.MONGO_PORT
    app.config['MONGODB_USERNAME'] = config.MONGO_USER
    app.config['MONGODB_PASSWORD'] = config.MONGO_PASS
    mongo.init_app(app)

    # Loading login handler.
    app.config["JWT_SECRET_KEY"] = config.SECRET
    app.config["JWT_HEADER_NAME"] = config.JWT_HEADER_NAME
    jwt.init_app(app)

    # Loading celery config.
    celery.conf.update(app.config)
    app.config["CELERY_RESULT_BACKEND"] = config.CELERY_RESULT_BACKEND
    app.config["CELERY_BROKER_URL"] = config.CELERY_BROKER_URL

    def call(self, *args, **kwargs):
        """
        Main call.
        """
        with app.app_context():
            return self.run(*args, **kwargs)

    celery.Task.__call__ = call

    # Loading cache connector.
    app.config["REDIS_URL"] = config.REDIS_URI
    redis.init_app(app)

    # Creating an admin.
    # WARNING: This piece of code has been created for the demo.
    #          This user will be used for testing purposes.
    if config.ADMIN_USER and config.ADMIN_PASS:
        with app.app_context():
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
    api.init_app(app)

    # End of app factory.
    logger.info("App started!")
    return app


app = create_app()

if __name__ == "__main__":
    # Only for debugging while developing.
    app.run(host='0.0.0.0', debug=True, port=8080)
