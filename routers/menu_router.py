from aiogram import Router
from aiogram.filters import Command
from aiogram.types import Message
from aiogram.types import FSInputFile
from core import settings
from services.interfaces import RagServiceInterface


class MenuRouter:
    def __init__(self, service: RagServiceInterface) -> None:
        self._router = Router(name="menu_router")
        self._service = service
        self._register_services()

    def _register_services(self) -> None:
        @self._router.message(Command("menu"))
        async def menu_handler(message: Message):
            text = (
                "<b>Menu options:</b>\n"
                "<i>This bot demostrates:</i>\n"
                " - sending formatted text\n"
                " - sending photos and documents\n"
                " - sending answers from AI Agent\n"
                " - working with AI Agent in RAG Mode\n"
            )

            await message.answer(text, parse_mode="HTML")

        @self._router.message(Command("send_photo"))
        async def send_photo_handler(message: Message):
            cat = FSInputFile(settings.MEDIA_DIR / "cat.jpg")

            await message.answer_photo(
                photo=cat, parse_mode="HTML", caption="<b> Here's you kitty </b>"
            )

        @self._router.message(Command("help"))
        async def help_handler(message: Message):
            text = (
                "<b>Help:</b>\n\n"
                "/start"
                " - start using bot\n"
                "/menu"
                " -  get the bot menu\n"
                "/send_photo"
                " - ask bot to sent you a photo\n"
                "/guide"
                " - get the guide.txt\n"
                "/promo"
                " - get a today's promo for evening\n"
                "/toggle_rag"
                " - turn on or off RAG AI Mode\n"
                "/rag_status"
                " - check current RAG AI Mode status\n"

            )

            await message.answer(text, parse_mode="HTML")

        @self._router.message(Command("guide"))
        async def help_doc_handler(message: Message):
            guide = FSInputFile(settings.MEDIA_DIR / "guide.txt")

            await message.answer_document(guide, parse_mode="HTML")

        @self._router.message(Command("promo"))
        async def promo_handler(message: Message):
            discount = FSInputFile(settings.MEDIA_DIR / "discount.jpg")
            text = (
                "Today's menu:\n"
                " - orange juice\n"
                " - hamburger\n"
                " - big beefstake\n"
                "Old price <s> 100 $ </s>\n"
                "Discount  20 $\n"
                "Total <b> 80 $ </b>\n"
            )

            await message.answer_document(discount, parse_mode="HTML")
            await message.answer(text, parse_mode="HTML")

        @self._router.message(Command("toggle_rag"))
        async def toggle_rag_mode(message: Message):
            args = message.text.split()
            if len(args) < 2:
                await message.answer("Incorrect values. Usage: /toggle_rag on[off]")
                return
            text = args[1].lower()
            if text == "on":
                set_value = True
            elif text == "off":
                set_value = False
            else:
                await message.answer("Incorrect values. Usage: /toggle_rag on[off]")
                return

            result = await self._service.toggle(user_id=message.from_user.id, value=set_value)
            response = "RAG mode enabled" if result else "RAG mode disabled"

            await message.answer(response)

        @self._router.message(Command("rag_status"))
        async def get_rag_status(message: Message):
            value = await self._service.get_status(user_id=message.from_user.id)

            response = "RAG is enabled" if value else "RAG mode disabled"
            await message.answer(response)

    def get_router(self) -> Router:
        return self._router
