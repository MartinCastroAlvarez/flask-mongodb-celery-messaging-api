"""
Main Flask app.
Run this script when executing the web server.

This file is required by the Docker image:
https://github.com/tiangolo/uwsgi-nginx-flask-docker
"""

from app import create_app, config

app = create_app()

if __name__ == "__main__":
    app.run(host=config.RUNSERVER_HOST,
            debug=config.RUNSERVER_DEBUG,
            port=config.RUNSERVER_PORT)
