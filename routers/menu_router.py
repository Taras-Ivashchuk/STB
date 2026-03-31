from aiogram import Router
from aiogram.filters import Command
from aiogram.types import Message
from aiogram.types import FSInputFile
from core import settings


class MenuRouter:
    def __init__(self, rag_router: Router) -> None:
        self._router = Router(name="menu_router")
        self._register_services()
        self._router.include_router(rag_router)

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
                "/rag_toggle on/off"
                " - turn on or off RAG AI Mode\n"
                "/rag_status"
                " - check current RAG AI Mode status\n"
                "/rag_docs"
                " - list user documents uploaded for RAG AI Mode\n"
                "/rag_doc_delete filename"
                " - delete document from RAG AI Mode\n"

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

    def get_router(self) -> Router:
        return self._router
