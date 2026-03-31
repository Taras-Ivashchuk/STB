from aiogram import Router
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

    def get_router(self) -> Router:
        return self._router