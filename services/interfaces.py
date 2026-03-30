from typing import Protocol, Any, BinaryIO

from models.agent import AgentResponse


class ServiceInterface(Protocol):
    """Service for using an agent in Telegram"""

    async def handle(self, user_id: int, msg: Any) -> AgentResponse:
        """Handle user message with AI Agent"""


class RagServiceInterface(Protocol):
    """Rag Service for AI Agent"""

    async def get_status(self, user_id: int) -> bool:
        """Get the RAG status"""

    async def toggle(self, user_id: int, value: bool) -> bool:
        """Turn on/off the RAG"""

    async def upload_pdf(self, user_id: int, filename: str, pdf_file: BinaryIO) -> None:
        """Upload pdf to vector database"""

    async def query(self, user_id: int, question: str, n_results: int = 10) -> AgentResponse:
        """Query the AI agent using RAG"""
