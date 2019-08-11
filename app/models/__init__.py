"""
Application models.

This classes are responsible for interacting
with the database. No authentication or business
logic is performed here.
"""

# pylint: disable=invalid-name

from flask_mongoengine import MongoEngine

mongo = MongoEngine()
