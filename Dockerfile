# This Dockerfile was copied from:
# https://ianlondon.github.io/blog/deploy-flask-docker-nginx/
FROM tiangolo/uwsgi-nginx-flask:python3.6

# Copy over our requirements.txt file
COPY requirements.txt /tmp/

# Upgrade pip and install required python packages
RUN pip install -U pip
RUN pip install -r /tmp/requirements.txt

# Allow Python to discover all files.
ENV PYTHONPATH="/"

# Copy over our app code
COPY ./app /app
