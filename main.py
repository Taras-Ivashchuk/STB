import asyncio

from factory import (
    get_agent,
    get_repository,
    get_model,
    get_service,
    get_bot,
    get_dispatcher,
    get_text_router,
    get_db_client,
    get_menu_router,
    get_rag_service,
    get_media_router,
    get_vector_db_client,
    get_vector_db_collection, get_vector_repository
)


async def main() -> None:
    mistral_model = get_model()
    pydantic_agent = get_agent(mistral_model)

    db_client = get_db_client()
    vector_db_client = await get_vector_db_client()
    vector_db_collection = await get_vector_db_collection(client=vector_db_client)
    vector_repository = get_vector_repository(db_client=vector_db_client, collection=vector_db_collection)

    user_history_repository = get_repository(db_client, db_prefix="history")
    user_rag_history_repository = get_repository(db_client, db_prefix="rag_history")
    user_settings_repository = get_repository(db_client, db_prefix="settings")

    rag_service = get_rag_service(
        settings_repository=user_settings_repository,
        vector_repository=vector_repository,
        history_repository=user_rag_history_repository,
        agent=pydantic_agent
    )

    chat_service = get_service(
        agent=pydantic_agent,
        repository=user_history_repository,
        rag_service=rag_service
    )

    basic_router = get_text_router(chat_service)
    menu_router = get_menu_router(rag_service)
    media_router = get_media_router(rag_service)

    routers = [menu_router, basic_router, media_router]

    dispatcher = get_dispatcher(routers, user_history_repository)
    bot = get_bot()

    await bot.delete_webhook(drop_pending_updates=True)
    await dispatcher.start_polling(bot)


if __name__ == "__main__":
    asyncio.run(main())
