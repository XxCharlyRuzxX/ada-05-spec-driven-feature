"""Custom domain exceptions for the customer service."""


class InvalidQueryException(Exception):
    """Exception raised when search query violates business rules."""

    def __init__(self, detail: str = "Query string must be at least 2 characters long"):
        self.detail = detail
        super().__init__(detail)
