"""
App validations

The libraries in this directory are responsible
for validating queries and raising the proper exceptions.
"""

from app.exceptions.form import EmptyQueryException


class QueryValidation:
    """
    This class is responsible for
    validating that a query is correct.
    """

    @classmethod
    def validate(cls, query: dict) -> None:
        """
        This function validates that the query is not empty.
        NOTE: The query is passed by reference.
        """
        if not isinstance(query, dict):
            raise EmptyQueryException()
