"""
App validations

The libraries in this directory are responsible
for validating queries and raising the proper exceptions.
"""

from app.validations import QueryValidation


class PaginationQueryValidation(QueryValidation):
    """
    This class is responsible for
    validating that a query is correct.
    """

    START = "start"
    LIMIT = "limit"

    @classmethod
    def validate(cls, query: dict) -> None:
        """
        This function validates that the
        query is valid to search objects.
        NOTE: The query is passed by reference.
        """
        QueryValidation.validate(query)
        if not query.get(cls.LIMIT) or\
           not isinstance(query[cls.LIMIT], int) or\
           query[cls.LIMIT] < 1:
            query[cls.LIMIT] = 100
        if query.get(cls.START) and not isinstance(query[cls.START], str):
            query[cls.START] = ""
