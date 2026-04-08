from threading import Thread
from unittest.mock import AsyncMock

from fakeredis import (
    TcpFakeServer,
    FakeAsyncRedis
)
import redis
import pytest

from repositories.redis_repository import RedisRepository


def test_redis_health():
    server_address = ("127.0.0.1", 6379)
    server = TcpFakeServer(server_address, server_type="redis")
    t = Thread(target=server.serve_forever, daemon=True)
    t.start()

    r = redis.Redis(host=server_address[0], port=server_address[1])
    r.set("foo", "bar")
    assert r.get("foo") == b"bar"

    # When you are done with the server, you can stop it with:
    server.shutdown()
    server.server_close()
    t.join()


class TestRedisRepository:
    prefix = "test"

    @pytest.fixture(scope="class")
    def redis_client(self):  # runs only once
        yield FakeAsyncRedis()

    @pytest.fixture(scope="class")  # runs only once
    def repo(self, redis_client):
        repo = RedisRepository(redis_client=redis_client, prefix=self.prefix)

        yield repo

    @pytest.mark.asyncio
    async def test_repo_save(self, repo, redis_client):
        """Should save item into redis database"""

        user_id = 1
        expected = b"hello world"

        await repo.save(user_id=user_id, item=expected)
        actual = await redis_client.get(f"{self.prefix}:{str(user_id)}")
        assert expected == actual

    @pytest.mark.asyncio
    async def test_repo_load(self, repo, redis_client):
        """Should load item from redis database"""

        user_id = 1
        expected = b"hello world"

        await redis_client.set(f"{self.prefix}:{str(user_id)}", expected)
        actual = await repo.load(user_id)
        assert expected == actual

    @pytest.mark.asyncio
    async def test_repo_delete(self, repo, redis_client):
        """Should delete user items from redis database"""

        user_id = 1
        expected = b"hello world"

        await redis_client.set(f"{self.prefix}:{str(user_id)}", expected)
        actual = await redis_client.get(f"{self.prefix}:{str(user_id)}")
        assert expected == actual

        await repo.delete(user_id)
        actual = await redis_client.get(f"{self.prefix}:{str(user_id)}")
        assert expected != actual

    @pytest.mark.asyncio
    async def test_repo_close_conection(self, repo, redis_client):
        """Should close connection to redis database"""

        redis_client.aclose = AsyncMock()
        await repo.close()

        redis_client.aclose.assert_called_once()
