from agent.interfaces import AgentInterface
from models.agent import AgentResponse
from repositories.interfaces import RepositoryInterface, VectorDbInterface
import json
from typing import BinaryIO, Any
from service_helpers.pdf_processor import PdfProcessor
from service_helpers.recursive_text_splitter import RecursiveLangChainTextSplitter
from app_logger import logger


class RagService:
    def __init__(
        self,
        settings_repository: RepositoryInterface,
        vector_repository: VectorDbInterface,
        history_repository: RepositoryInterface,
        agent: AgentInterface,
    ) -> None:
        self._settings_repository = settings_repository
        self._vector_repository = vector_repository
        self._history_repository = history_repository
        self._agent = agent

    async def get_status(self, user_id: int) -> bool:
        raw_settings = await self._settings_repository.load(user_id=user_id)
        settings = json.loads(raw_settings) if raw_settings else {}

        return settings.get("rag_status", False)

    async def toggle(self, user_id: int, value: bool) -> bool:
        raw_settings = await self._settings_repository.load(user_id=user_id)
        settings = json.loads(raw_settings) if raw_settings else {}
        settings["rag_status"] = value

        await self._settings_repository.save(user_id=user_id, item=json.dumps(settings))

        return value

    async def upload_pdf(self, user_id: int, filename: str, pdf_file: BinaryIO) -> None:
        pdf_processor = PdfProcessor()
        text_splitter = RecursiveLangChainTextSplitter()
        pdf_result = await pdf_processor.parse_pdf(text_splitter=text_splitter, filename=filename, pdf_file=pdf_file)
        await self._vector_repository.add_documents(user_id=user_id, pdf_result=pdf_result)

    async def query(self, user_id: int, question: str, n_results: int = 10) -> AgentResponse:
        search_results = await self._vector_repository.search(
            user_id=user_id,
            question=question,
            n_results=n_results
        )

        if not search_results["documents"][0] or not search_results["metadatas"][0]:
            return AgentResponse(response="I don't have any context", history=bytes())

        context = self.format_context(
            documents=search_results["documents"][0],
            metadatas=search_results["metadatas"][0]
        )
        prompt = ("- Use only the context and message history\n"
                  "- Be strict while answering the queries\n"
                  "- If the answer cannot be found in the context, respond with: 'I can only answer questions based on the uploaded documents'\n"
                  "- Do not use any outside knowledge beyond what is in the context\n"
                  "- Be strict and not creative\n"
                  "- Consider the history as a part of the context provided\n"
                  "- Use agent response model for responses\n"
                  
                  f"- Here is the context: {context}"
                  )

        user_history = await self._history_repository.load(user_id=user_id)
        agent_response = await self._agent.ask(question=question, history=user_history, instructions=prompt)
        logger.debug(agent_response.history.decode("utf-8"))

        await self._history_repository.save(user_id=user_id, item=agent_response.history)

        return agent_response

    def format_context(self, documents: list[str], metadatas: list[dict[Any, Any]]) -> str:

        ctx_parts = []
        for i, (document, metadata) in enumerate(zip(documents, metadatas), 1):
            filename = metadata.get("filename", "unknown")
            chunk = metadata.get("chunk_index", "unknown")
            ctx_part = f"[Document #: {i}, Source: {document}, Filename: {filename}, Chunk: {chunk}]\n{document}\n"
            ctx_parts.append(ctx_part)

        return "\n".join(ctx_parts)

    async def get_all_filenames(self, user_id: int) -> list[str]:
        return await self._vector_repository.get_all_filenames(user_id=user_id)

    async def count_documents(self, user_id: int) -> int:
        return await self._vector_repository.count_documents(user_id=user_id)
