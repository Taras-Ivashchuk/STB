from typing import Protocol, Any


class ServiceInterface(Protocol):
    """Service for using an agent in Telegram"""

    async def handle(self, user_id: int, msg: Any) -> Any: ...


class RagServiceInterface(Protocol):
    """Rag Service for AI Agent"""

    async def get_status(self, user_id: int) -> bool:
        ...

    async def toggle(self, user_id: int, value: bool) -> bool:
        ...
