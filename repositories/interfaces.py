from typing import Protocol, Any, Dict

from dtos import PdfResult


class RepositoryInterface(Protocol):
    async def save(self, user_id: int, item: Any) -> None:
        """Save the item by user id"""

    async def load(self, user_id: int) -> Any:
        """Load the item by user id"""

    async def close(self) -> None:
        """Close the connection"""


class VectorDbInterface(Protocol):
    async def add_documents(self, user_id: int, pdf_result: PdfResult) -> None:
        """Add documents to vector database"""

    async def search(
        self,
        user_id: int,
        question: str,
        n_results: int = 10
    ) -> Dict[Any, Any]:
        """Search documents in vector db using vector similarity"""

    async def delete_by_filename(self, user_id: int, filename: str) -> None:
        """Delete document by filename in vector database"""

    async def get_all_filenames(self, user_id: int) -> list[str]:
        """Get all filenames from vector database"""

    async def count_documents(self, user_id: int) -> int:
        """Count all documents in vector database"""
