from typing import Protocol, Any


class RepositoryInterface(Protocol):
    async def save(self, user_id: int, history: Any) -> None:
        """Save history for user with id"""

    async def load(self, user_id) -> list | None:
        """Load the user history by id"""

    async def close(self) -> None:
        """Close the connection"""
