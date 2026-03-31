from chromadb import (
    AsyncClientAPI,
    QueryResult
)
from chromadb.api.models.AsyncCollection import AsyncCollection

from dtos import PdfResult


class ChromaRepository:
    def __init__(self, db: AsyncClientAPI, collection: AsyncCollection) -> None:
        self._db = db
        self._collection = collection

    @classmethod
    async def create(cls, db: AsyncClientAPI, collection_name: str) -> "ChromaRepository":
        collection = await db.get_or_create_collection(name=collection_name)
        return cls(db, collection)

    async def add_documents(self, user_id: int, pdf_result: PdfResult) -> None:
        ids = []
        metadatas = []

        for i, sentence in enumerate(pdf_result.sentences):
            ids.append(f"{pdf_result.file_name} - {i}")
            metadatas.append(
                {
                    "user_id": user_id,
                    "filename": pdf_result.file_name,
                    "chunk_index": i
                }
            )

        await self._collection.add(ids=ids, documents=pdf_result.sentences, metadatas=metadatas)

    async def search(
        self,
        user_id: int,
        question: str,
        n_results: int = 10
    ) -> QueryResult:
        result = await self._collection.query(
            query_texts=[question],
            n_results=n_results,
            where={"user_id": user_id}
        )

        return result

    async def delete_by_filename(self, user_id: int, filename: str) -> None:
        await self._collection.delete(where={"user_id": user_id, "filename": filename})

    async def get_all_filenames(self, user_id: int) -> list[str]:
        result = await self._collection.get(where={"user_id": user_id}, include=["metadatas"])
        filenames = set()

        for file_metadata in result.get("metadatas", []):
            file_metadata: dict
            if "filename" in file_metadata:
                filenames.add(file_metadata["filename"])

        return sorted(list(filenames))

    async def count_documents(self, user_id: int) -> int:
        result = await self._collection.get(where={"user_id": user_id})

        return len(result.get("documents", []))
