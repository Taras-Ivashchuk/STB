from aiogram import Router, F, html
from aiogram.filters import CommandStart
from aiogram.types import Message
from services.interfaces import ServiceInterface


class TextRouter:
    def __init__(self, service: ServiceInterface) -> None:
        self._router = Router(name="tg_text_router")
        self._service = service
        self._register_services()

    def _register_services(self) -> None:
        @self._router.message(CommandStart())
        async def command_start_handler(message: Message) -> None:
            await message.answer(f"Hello, {html.bold(message.from_user.full_name)}!")  # type: ignore

        @self._router.message(F.text, lambda mes: "hello" in mes.text.lower())
        async def text_hello_handler(message: Message) -> None:
            try:
                await message.answer("How are you today?")
            except TypeError:
                await message.answer("Nice try!")

        @self._router.message(F.text)
        async def text_handler(message: Message) -> None:
            try:
                if not message.text:
                    return
                response = await self._service.handle(
                    user_id=message.from_user.id, msg=message.text
                )
                await message.answer(response)
            except TypeError:
                await message.answer("Nice try!")

    def get_router(self) -> Router:
        return self._router
