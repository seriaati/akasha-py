from __future__ import annotations

__all__ = ("DESC_TO_ERROR", "AkashaAPIError", "UIDNotFoundError")


class AkashaAPIError(Exception):
    """Base class for all Akasha API errors."""

    def __init__(self, title: str, description: str) -> None:
        self.title = title
        self.description = description

    def __str__(self) -> str:
        return f"{self.title}: {self.description}"

    def __repr__(self) -> str:
        return f"{self.__class__.__name__}({self.title!r}, {self.description!r})"


class UIDNotFoundError(AkashaAPIError):
    """Raised when the provided UID cannot be fetched from Enka Network API."""


class IncorrectUIDFormatError(AkashaAPIError):
    """Raised when the provided UID is not in the correct format."""


class InvalidAPIRequestError(AkashaAPIError):
    """Raised when the API request is invalid."""


DESC_TO_ERROR = {
    "Provided UID cannot be fetched from Enka Network API": UIDNotFoundError,
    "The UID format is incorrect": IncorrectUIDFormatError,
}
