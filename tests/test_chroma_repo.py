import chromadb
import pytest
from chromadb import QueryResult
from testcontainers.chroma import ChromaContainer

from dtos import PdfResult
from exceptions import DocumentNotFoundError
from repositories.chroma_repository import ChromaRepository


class TestChromaRepository:
    collection_name = "test"

    @pytest.fixture(scope="class")
    async def chroma_container(self):
        """Get Chroma db connection"""
        with ChromaContainer("chromadb/chroma:latest") as chroma:
            config = chroma.get_config()

            yield await chromadb.AsyncHttpClient(
                host=config["host"],
                port=config["port"]
            )

    @pytest.fixture(scope="class")
    async def chroma_collection(self, chroma_container):
        yield await chroma_container.get_or_create_collection(name=self.collection_name)

    @pytest.fixture(scope="class")
    async def chroma_repo(self, chroma_container, chroma_collection):
        yield ChromaRepository(db=chroma_container, collection=chroma_collection)

    @pytest.mark.asyncio
    async def test_chroma_add_document(self, chroma_repo, chroma_collection):
        user_id = 1
        expected_chunk = "first_faux_chunk"
        expected_filename = "faux.pdf"

        faux_pdf_result = PdfResult(file_name=expected_filename, sentences=[expected_chunk])
        await chroma_repo.add_documents(user_id=user_id, pdf_result=faux_pdf_result)

        actual = await chroma_collection.query(
            query_texts=[expected_filename],
            n_results=1,
            where={"user_id": user_id}
        )

        actual_chunk = actual["documents"][0][0]
        actual_filename = actual["metadatas"][0][0]["filename"]

        assert actual_chunk == expected_chunk
        assert actual_filename == expected_filename

    @pytest.mark.asyncio
    async def test_chroma_search_document(self, chroma_repo, chroma_collection):
        user_id = 1
        expected_chunk = "first_faux_chunk"
        expected_filename = "faux.pdf"
        faux_pdf_result = PdfResult(file_name=expected_filename, sentences=[expected_chunk])

        ids = []
        metadatas = []

        for i, sentence in enumerate(faux_pdf_result.sentences):
            ids.append(f"{faux_pdf_result.file_name} - {i}")
            metadatas.append(
                {
                    "user_id": user_id,
                    "filename": faux_pdf_result.file_name,
                    "chunk_index": i
                }
            )

        await chroma_collection.add(ids=ids, documents=faux_pdf_result.sentences, metadatas=metadatas)

        actual = await chroma_repo.search(user_id=user_id, question=expected_chunk, n_results=1)

        assert actual["documents"][0][0] == expected_chunk

    @pytest.mark.asyncio
    async def test_chroma_delete_by_filename_raises_error(self, chroma_repo):
        with pytest.raises(DocumentNotFoundError):
            await chroma_repo.delete_by_filename(user_id=1, filename="not existing")

    @pytest.mark.asyncio
    async def test_chroma_delete_by_filename_sucess(self, chroma_repo, chroma_collection):
        user_id = 1
        expected_chunk = "first_faux_chunk"
        expected_filename = "faux.pdf"
        faux_pdf_result = PdfResult(file_name=expected_filename, sentences=[expected_chunk])

        ids = []
        metadatas = []

        for i, sentence in enumerate(faux_pdf_result.sentences):
            ids.append(f"{faux_pdf_result.file_name} - {i}")
            metadatas.append(
                {
                    "user_id": user_id,
                    "filename": faux_pdf_result.file_name,
                    "chunk_index": i
                }
            )

        await chroma_collection.add(ids=ids, documents=faux_pdf_result.sentences, metadatas=metadatas)

        await chroma_repo.delete_by_filename(user_id=user_id, filename=expected_filename)
        actual = await chroma_collection.query(
            query_texts=[expected_filename],
            n_results=1,
            where={"user_id": user_id}
        )

        actual_chunk = actual["documents"][0]
        actual_filename = actual["metadatas"][0]

        assert actual_chunk == []
        assert actual_filename == []

    @pytest.mark.asyncio
    async def test_get_all_filenames(self, chroma_repo, chroma_collection):
        user_id = 1
        expected_chunks1 = ["first_faux_chunk1", "second_faux_chunk1"]
        expected_filename1 = "faux1.pdf"
        faux_pdf_result1 = PdfResult(file_name=expected_filename1, sentences=expected_chunks1)

        expected_chunks2 = ["first_faux_chunk2", "second_faux_chunk2"]
        expected_filename2 = "faux2.pdf"
        faux_pdf_result2 = PdfResult(file_name=expected_filename2, sentences=expected_chunks2)

        for faux_pdf_result in [faux_pdf_result1, faux_pdf_result2]:
            ids = []
            metadatas = []

            for i, sentence in enumerate(faux_pdf_result.sentences):
                ids.append(f"{faux_pdf_result.file_name} - {i}")
                metadatas.append(
                    {
                        "user_id": user_id,
                        "filename": faux_pdf_result.file_name,
                        "chunk_index": i
                    }
                )
            await chroma_collection.add(ids=ids, documents=faux_pdf_result.sentences, metadatas=metadatas)

        actual = await chroma_repo.get_all_filenames(user_id=user_id)

        assert actual == list(sorted([expected_filename1, expected_filename2]))

    @pytest.mark.asyncio
    async def test_chroma_count_document(self, chroma_repo, chroma_collection):
        user_id = 1
        expected_chunks1 = ["first_faux_chunk1", "second_faux_chunk1"]
        expected_filename1 = "faux1.pdf"
        faux_pdf_result1 = PdfResult(file_name=expected_filename1, sentences=expected_chunks1)

        expected_chunks2 = ["first_faux_chunk2", "second_faux_chunk2"]
        expected_filename2 = "faux2.pdf"
        faux_pdf_result2 = PdfResult(file_name=expected_filename2, sentences=expected_chunks2)

        for faux_pdf_result in [faux_pdf_result1, faux_pdf_result2]:
            ids = []
            metadatas = []

            for i, sentence in enumerate(faux_pdf_result.sentences):
                ids.append(f"{faux_pdf_result.file_name} - {i}")
                metadatas.append(
                    {
                        "user_id": user_id,
                        "filename": faux_pdf_result.file_name,
                        "chunk_index": i
                    }
                )
            await chroma_collection.add(ids=ids, documents=faux_pdf_result.sentences, metadatas=metadatas)

        actual = await chroma_repo.count_documents(user_id=user_id)

        assert actual == len(expected_chunks1 + expected_chunks2)

    @pytest.mark.asyncio
    async def test_chroma_delete_all_documents(self, chroma_repo, chroma_collection):
        user_id = 1
        expected_chunks1 = ["first_faux_chunk1", "second_faux_chunk1"]
        expected_filename1 = "faux1.pdf"
        faux_pdf_result1 = PdfResult(file_name=expected_filename1, sentences=expected_chunks1)

        expected_chunks2 = ["first_faux_chunk2", "second_faux_chunk2"]
        expected_filename2 = "faux2.pdf"
        faux_pdf_result2 = PdfResult(file_name=expected_filename2, sentences=expected_chunks2)

        for faux_pdf_result in [faux_pdf_result1, faux_pdf_result2]:
            ids = []
            metadatas = []

            for i, sentence in enumerate(faux_pdf_result.sentences):
                ids.append(f"{faux_pdf_result.file_name} - {i}")
                metadatas.append(
                    {
                        "user_id": user_id,
                        "filename": faux_pdf_result.file_name,
                        "chunk_index": i
                    }
                )
            await chroma_collection.add(ids=ids, documents=faux_pdf_result.sentences, metadatas=metadatas)

        await chroma_repo.delete_all_documents(user_id=user_id)

        actual = await chroma_collection.query(
            query_texts=expected_chunks1 + expected_chunks2,
            n_results=1,
            where={"user_id": user_id}
        )

        assert [el for row in actual["documents"][0] for el in row] == []
