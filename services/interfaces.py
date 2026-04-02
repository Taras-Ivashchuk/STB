from typing import Protocol, Any, BinaryIO

from models.agent import AgentResponse


class ServiceInterface(Protocol):
    """Service for using an agent in Telegram"""

    async def handle(self, user_id: int, msg: Any) -> AgentResponse:
        """Handle user message with AI Agent"""

    async def reset(self, user_id: int) -> None:
        """Reset user settings, remove history and uploaded documents"""


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

    async def get_all_filenames(self, user_id: int) -> list[str]:
        """Get all filenames of documents that were uploaded by user"""

    async def count_documents(self, user_id: int) -> int:
        """Count the documents that were uploaded by user"""

    async def delete_all_documents(self, user_id: int) -> None:
        """Delete all user documents"""

    async def delete_all(self, user_id: int) -> None:
        """Delete all user documents, all user settings and all user history"""