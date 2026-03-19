from typing import Any
from redis.asyncio import Redis


class RedisRepository:
    def __init__(self, redis_client: Redis):
        self._connection = redis_client

    async def save(self, user_id: int, history: Any) -> None:
        await self._connection.set(str(user_id), history)

    async def load(self, user_id: int):
        return await self._connection.get(str(user_id))

    async def close(self) -> None:
        await self._connection.aclose()
