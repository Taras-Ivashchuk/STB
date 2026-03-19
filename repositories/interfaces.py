from typing import Protocol, Any


class RepositoryInterface(Protocol):
    async def save(self, user_id: int, item: Any) -> None:
        """Save the item by user id"""

    async def load(self, user_id) -> Any:
        """Load the item by user id"""

    async def close(self) -> None:
        """Close the connection"""
