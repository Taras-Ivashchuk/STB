from typing import Any
from redis.asyncio import Redis


class RedisRepository:
    def __init__(self, redis_client: Redis, prefix: str):
        self._connection = redis_client
        self._prefix = prefix

    async def save(self, user_id: int, item: Any) -> None:
        await self._connection.set(f"{self._prefix}:{str(user_id)}", item)

    async def load(self, user_id: int) -> Any:
        return await self._connection.get(f"{self._prefix}:{str(user_id)}")

    async def close(self) -> None:
        await self._connection.aclose()
