from typing import Any

from agent.interfaces import AgentInterface
from app_logger import logger
from repositories.interfaces import RepositoryInterface


class ChatService:
    def __init__(self, agent: AgentInterface, repository: RepositoryInterface) -> None:
        self._agent = agent
        self._repository = repository

    async def handle(self, user_id: int, msg: str) -> str:
        user_history = await self._repository.load(user_id=user_id)

        # agent deserializes the user history and returns a serialized response
        agent_response = await self._agent.ask(question=msg, history=user_history)
        logger.debug(agent_response.history.decode("utf-8"))

        # store the serialized history in repository
        await self._repository.save(user_id=user_id, history=agent_response.history)

        return agent_response.response
