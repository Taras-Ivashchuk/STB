import io
import unittest
from unittest.mock import AsyncMock

import pytest
import json

from core.settings import BASE_DIR
from models.agent import AgentResponse
from services.rag_service import RagService


class TestRagService:
    @pytest.fixture(scope="class")
    def rag_service(self):
        mock_settings_repository = AsyncMock()
        mock_vector_repository = AsyncMock()
        mock_history_repository = AsyncMock()
        mock_agent = AsyncMock()

        # configure mock objects
        mock_settings_repository.load.return_value = json.dumps({"rag_status": True})

        yield RagService(
            settings_repository=mock_settings_repository,
            vector_repository=mock_vector_repository,
            history_repository=mock_history_repository,
            agent=mock_agent
        )
        print("Rag service destroyed")

    @pytest.mark.asyncio
    async def test_get_status(self, rag_service):
        """Should return current RAG mode status for user"""
        assert await rag_service.get_status(user_id=1) == True

    @pytest.mark.asyncio
    async def test_toggle(self, rag_service):
        """Should toggle RAG mode for user"""
        assert await rag_service.toggle(user_id=1, value=False) == False

    @pytest.mark.asyncio
    async def test_uplod_pdf(self, rag_service):
        """Should upload the pdf user file for RAG mode"""

        user_id = 1
        filename = "sample.pdf"
        filepath = BASE_DIR / "tests" / filename

        with open(filepath, mode="br") as file_in:
            pdf_bytes = file_in.read()
            pdf_bytes = io.BytesIO(pdf_bytes)

            await rag_service.upload_pdf(user_id, filename, pdf_file=pdf_bytes)

            rag_service._vector_repository.add_documents.assert_awaited_once()

    @pytest.mark.asyncio
    async def test_query_no_documents(self, rag_service):
        """Should return response when no documents uploaded"""

        rag_service._vector_repository.search.return_value = {
            "documents": [[]]
        }

        expected_message = "I don't have any context"
        response = await rag_service.query(user_id=1, question="How are you?")

        assert response.response == expected_message

    @pytest.mark.asyncio
    async def test_query_documents_uploaded(self, rag_service):
        """Should return relevant response when documents uploaded"""

        question = "How are you?"
        rag_service._agent.ask.return_value = AgentResponse(response="Fine", history=bytes())

        rag_service._vector_repository.search.return_value = {
            "documents": [["first_document"]],
            "metadatas": [[{
                "filename": "test"
            }]]
        }

        response = await rag_service.query(user_id=1, question=question)

        assert isinstance(response, AgentResponse)

        rag_service._history_repository.load.assert_awaited_once()
        rag_service._history_repository.save.assert_awaited_once()
        rag_service._agent.ask.assert_awaited_once()

        rag_service._agent.ask.assert_awaited_once_with(
            question=question,
            history=unittest.mock.ANY,
            instructions=unittest.mock.ANY
        )

    @pytest.mark.asyncio
    async def test_get_all_filenames(self, rag_service):
        """Should return filenames of uploaded user documents"""

        filenames = ["sample1.pdf", "sample2.pdf"]
        rag_service._vector_repository.get_all_filenames.return_value = filenames

        response = await rag_service.get_all_filenames(user_id=1)

        assert response == filenames

    @pytest.mark.asyncio
    async def test_delete_all(self, rag_service):
        """Should delete all user settings, documents and history"""

        user_id = 2
        await rag_service.delete_all(user_id=user_id)

        rag_service._vector_repository.delete_all_documents.assert_awaited_once_with(user_id=user_id)
        rag_service._history_repository.delete.assert_awaited_once_with(user_id)
        rag_service._settings_repository.delete.assert_awaited_once_with(user_id)
