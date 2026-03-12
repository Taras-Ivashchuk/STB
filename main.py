import asyncio

from factory import (
    get_agent,
    get_repository,
    get_model,
    get_service,
    get_bot,
    get_dispatcher,
    get_text_router,
)
from routers.media_handlers import router as media_router
from routers.menu_handlers import router as menu_router


async def main() -> None:
    mistral_model = get_model()
    pydantic_agent = get_agent(mistral_model)
    redis_repository = get_repository()
    chat_service = get_service(agent=pydantic_agent, repository=redis_repository)
    basic_router = get_text_router(chat_service)
    routers = [menu_router, basic_router, media_router]

    dispatcher = get_dispatcher(routers, redis_repository)
    bot = get_bot()

    await bot.delete_webhook(drop_pending_updates=True)
    await dispatcher.start_polling(bot)


if __name__ == "__main__":
    asyncio.run(main())
