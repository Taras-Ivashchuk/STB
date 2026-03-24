import io

from aiogram import Router, F
from aiogram.types import Message

from services.interfaces import RagServiceInterface


class MediaRouter:
    def __init__(self, rag_service: RagServiceInterface) -> None:
        self._router = Router(name="tg_media_router")
        self._rag_service = rag_service
        self._register_handlers()

    def _register_handlers(self) -> None:
        @self._router.message(F.photo)
        async def photo_handler(message: Message) -> None:
            await message.answer(f"Cool! Nice photo. Photo id {message.photo[-1].file_id}")  # type: ignore

        @self._router.message(F.sticker)
        async def sticker_handler(message: Message) -> None:
            await message.answer("Cool! Nice sticker")

        @self._router.message(F.audio)
        async def audio_handler(message: Message) -> None:
            await message.answer("Cool! Nice audio")

        @self._router.message(F.document.mime_type.endswith("pdf"))
        async def pdf_handler(message: Message) -> None:
            rag_status = await self._rag_service.get_status(user_id=message.from_user.id)
            if rag_status:
                bin_file = await message.bot.download(file=message.document, destination=io.BytesIO())
                # await self._rag_service.upload_pdf(bin_file)
                await message.answer("Rag is On! Your document is uploaded to vector database")

            else:
                await message.answer("Rag is Off! Nice document")

    def get_router(self) -> Router:
        return self._router
