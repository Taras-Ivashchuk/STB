from typing import Protocol, Any


class ServiceInterface(Protocol):
    """Service for using an agent in Telegram"""

    async def handle(self, user_id: int, msg: Any) -> Any: ...
