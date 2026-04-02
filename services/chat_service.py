from typing import Optional

from agent.interfaces import AgentInterface
from app_logger import logger
from models.agent import AgentResponse
from repositories.interfaces import RepositoryInterface
from services.interfaces import RagServiceInterface


class ChatService:
    def __init__(
        self,
        agent: AgentInterface,
        repository: RepositoryInterface,
        rag_service: RagServiceInterface
    ) -> None:
        self._agent = agent
        self._repository = repository
        self._rag_service = rag_service

    async def handle(self, user_id: int, msg: str, n_results: Optional[int] = 10) -> AgentResponse:
        is_rag = await self._rag_service.get_status(user_id=user_id)

        if not is_rag:
            prompt = (
                "- Your task is to provide answers using user queries and message history\n"
                "- Be creative while answering the queries\n"
                "- If history is empty use only instructions provided\n"
                "- Consider the history as a part of the instructions provided\n"
                "- Use agent response model for responses\n"
            )

            user_history = await self._repository.load(user_id=user_id)

            # agent deserializes the user history and returns a serialized response
            agent_response = await self._agent.ask(question=msg, history=user_history, instructions=prompt)
            logger.debug(agent_response.history.decode("utf-8"))

            # store the serialized history in repository
            await self._repository.save(user_id=user_id, item=agent_response.history)
            return agent_response
        else:
            agent_response = await self._rag_service.query(user_id=user_id, question=msg, n_results=n_results)
            return agent_response

    async def reset(self, user_id: int) -> None:
        await self._repository.delete(user_id=user_id)
        await self._rag_service.delete_all(user_id=user_id)
        await self._rag_service.toggle(user_id=user_id, value=False)