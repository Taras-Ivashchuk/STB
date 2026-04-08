from unittest.mock import AsyncMock

import pytest

from models.agent import AgentResponse
from services import rag_service
from services.chat_service import ChatService


class TestChatService:
    @pytest.fixture(scope="class")
    async def chat_service(self):
        mock_agent = AsyncMock()
        mock_repository = AsyncMock()
        mock_rag_service = AsyncMock()

        yield ChatService(
            agent=mock_agent,
            repository=mock_repository,
            rag_service=mock_rag_service
        )

        print("chat service destroyed")

    @pytest.mark.asyncio
    async def test_handle_is_not_rag(self, chat_service):
        """Should return lax agent response"""

        user_id = 1
        message = "hello world"
        chat_service._rag_service.get_status.return_value = False
        faux_agent_response = AgentResponse(
            response="Hey ya",
            history=bytes(2)
        )
        chat_service._agent.ask.return_value = faux_agent_response

        response = await chat_service.handle(user_id=user_id, msg=message)

        assert response == faux_agent_response

        chat_service._repository.load.assert_awaited_once_with(user_id=user_id)
        chat_service._repository.save.assert_awaited_once_with(
            user_id=user_id,
            item=response.history
        )

    @pytest.mark.asyncio
    async def test_handle_rag_on(self, chat_service):
        """Should return strict agent response based on context"""

        faux_agent_response = AgentResponse(
            response="Hey ya",
            history=bytes(2)
        )
        chat_service._rag_service.query.return_value = faux_agent_response
        user_id = 1
        message = "How are you!"
        results_number = 20

        response = await chat_service.handle(
            user_id=user_id,
            msg=message,
            n_results=results_number
        )

        assert response == faux_agent_response
        chat_service._rag_service.query.assert_awaited_once_with(
            user_id=user_id,
            question=message,
            n_results=results_number
        )

    @pytest.mark.asyncio
    async def test_reset(self, chat_service):
        """Should delete user history, delete user RAG settings, turn off user RAG mode"""

        user_id = 10

        await chat_service.reset(user_id=user_id)

        chat_service._repository.delete.assert_awaited_once_with(
            user_id=user_id
        )
        chat_service._rag_service.delete_all.assert_awaited_once_with(
            user_id=user_id
        )
        chat_service._rag_service.toggle.assert_awaited_once_with(
            user_id=user_id,
            value=False,
        )
