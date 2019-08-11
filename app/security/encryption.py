"""
Security libraries.

These classes are responsible for ensuring
a certain degree of security in the app.
"""

import time
import random
import logging

import base64
import bcrypt

from app import config

logger = logging.getLogger(__name__)


class Hash:
    """
    Entity responsible for hashing
    and comparing hashed passwords.
    """

    @classmethod
    def obfuscate(cls, x: str) -> str:
        """
        Public class method to hash a string.
        """
        salt = base64.b64decode(config.SALT.encode(config.ENCODING))
        result = bcrypt.hashpw(x.encode(config.ENCODING), salt)
        return result.decode(config.ENCODING)

    @classmethod
    def match(cls, hashed_password: str, plain_text: str) -> bool:
        """
        Public class method to compare a hashed password and a raw string.
        This implements Fixed Time Comparisson security measures.
        """
        match = bcrypt.checkpw(plain_text.encode(config.ENCODING),
                               hashed_password.encode(config.ENCODING))
        if not match:
            sleep = random.uniform(*config.PASSWORD_FIXED_COMPARISSON_TIME)
            time.sleep(sleep)
            return False
        return True
