"""
Application exceptions.
"""

import logging

logger = logging.getLogger()


class IguazuException(Exception):
    """
    Core class for all app exceptions.
    """

    CODE = 500
    SUBCODE = 5000
    MESSAGE = "Unexpected Error"

    def __init__(self, *errors) -> None:
        """
        Initializing exception with custom errors.
        """
        Exception.__init__(self, *errors)
        self.__errors = errors
        logger.error("APP ERROR | sf_type=%s | sf_errors=%s", self, errors)

    @property
    def code(self) -> int:
        """
        Status code getter.
        """
        return self.CODE

    @property
    def subcode(self) -> int:
        """
        Subcode getter.
        """
        return self.SUBCODE

    def to_str(self) -> str:
        """
        String serializer.
        """
        return " ".join([
            self.MESSAGE,
            "".join([
                str(error)
                for error in self.__errors
            ])
        ]).strip()

    def to_json(self) -> dict:
        """
        JSON serializer.
        """
        return {
            "code": self.code,
            "type": "{}".format(self.__class__.__name__),
            "subcode": self.subcode,
            "error": self.to_str(),
        }
