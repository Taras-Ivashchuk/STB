from aiogram import Router, F
from aiogram.types import Message

router = Router(name="tg_media_router")


@router.message(F.photo)
async def photo_handler(message: Message) -> None:
    await message.answer(f"Cool! Nice photo. Photo id {message.photo[-1].file_id}")  # type: ignore


@router.message(F.sticker)
async def sticker_handler(message: Message) -> None:
    await message.answer("Cool! Nice sticker")


@router.message(F.audio)
async def audio_handler(message: Message) -> None:
    await message.answer("Cool! Nice audio")
