from aiogram import Router

from exceptions import DocumentNotFoundError
from services.interfaces import RagServiceInterface
from aiogram.filters import Command
from aiogram.types import Message


class RagRouter:
    def __init__(self, rag_service: RagServiceInterface) -> None:
        self._router = Router(name="rag_router")
        self._rag_service = rag_service
        self._register_services()

    def _register_services(self) -> None:
        @self._router.message(Command("rag_toggle"))
        async def toggle_rag_mode(message: Message):
            args = message.text.split()
            if len(args) < 2:
                await message.answer("Incorrect values. Usage: /rag_toggle on[off]")
                return
            text = args[1].lower()
            if text == "on":
                set_value = True
            elif text == "off":
                set_value = False
            else:
                await message.answer("Incorrect values. Usage: /rag_toggle on[off]")
                return

            result = await self._rag_service.toggle(user_id=message.from_user.id, value=set_value)
            response = "RAG mode enabled" if result else "RAG mode disabled"

            await message.answer(response)

        @self._router.message(Command("rag_status"))
        async def get_rag_status(message: Message):
            value = await self._rag_service.get_status(user_id=message.from_user.id)

            response = "RAG is enabled" if value else "RAG mode disabled"
            await message.answer(response)

        @self._router.message(Command("rag_docs"))
        async def get_rag_docs_uploaded(message: Message):
            rag_status = await self._rag_service.get_status(user_id=message.from_user.id)
            if not rag_status:
                await message.answer("RAG mode disabled")
                return
            user_id = message.from_user.id
            filenames = await self._rag_service.get_all_filenames(user_id=user_id)
            total_documents = await self._rag_service.count_documents(user_id=user_id)
            response = f"Total files: {len(filenames)}, total documents {total_documents}\n" + "\n".join(
                f"{i}. {filename}" for i, filename in enumerate(filenames, 1)
            )
            await message.answer(response)

        @self._router.message(Command("rag_doc_delete"))
        async def delete_doc_from_rag(message: Message):
            args = message.text.split()
            if len(args) < 2:
                await message.answer("Usage: /rag_delete_doc filename")
                return

            filename = args[1]
            user_id = message.from_user.id

            try:
                await self._rag_service.delete_by_filename(user_id=user_id, filename=filename)
            except DocumentNotFoundError:
                await message.answer(f"Error! File [{filename}] not found. Check the filename")
                return

            await message.answer(f"File [{filename}] successfuly deleted!")

    def get_router(self) -> Router:
        return self._router
