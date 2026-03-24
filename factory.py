import chromadb
from aiogram import Bot, Dispatcher, Router
from aiogram.client.default import DefaultBotProperties
from aiogram.enums import ParseMode
from chromadb import AsyncClientAPI
from pydantic_ai.models import Model
from httpx import AsyncClient
from pydantic_ai.models.mistral import MistralModel
from pydantic_ai.providers.mistral import MistralProvider

from agent.interfaces import AgentInterface
from agent.pydantic_agent import PydanticAgent
from repositories.interfaces import RepositoryInterface
from redis.asyncio import Redis

from repositories.redis_repository import RedisRepository
from routers.media_router import MediaRouter
from routers.menu_router import MenuRouter
from routers.text_router import TextRouter
from services.chat_service import ChatService
from services.interfaces import ServiceInterface, RagServiceInterface
from core.settings import settings
from typing import Any, Coroutine

from services.rag_service import RagService


def get_model() -> Model:
    custom_http_client = AsyncClient(timeout=30)
    return MistralModel(
        "mistral-small-latest",
        provider=MistralProvider(
            api_key=settings.MISTRAL_API_KEY, http_client=custom_http_client
        ),
    )


def get_agent(model: Model) -> AgentInterface:
    return PydanticAgent(llm_model=model)


def get_db_client() -> Any:
    return Redis(host=settings.DB_HOST, port=settings.DB_PORT)


def get_repository(db_client: Any, db_prefix: str) -> RepositoryInterface:
    return RedisRepository(redis_client=db_client, prefix=db_prefix)


def get_service(
    agent: AgentInterface,
    repository: RepositoryInterface,
    rag_service: RagServiceInterface
) -> ServiceInterface:
    return ChatService(agent=agent, repository=repository, rag_service=rag_service)


def get_rag_service(settings_repository: RepositoryInterface) -> RagServiceInterface:
    return RagService(settings_repository=settings_repository)


def get_bot() -> Bot:
    bot = Bot(
        token=settings.BOT_TOKEN,
        default=DefaultBotProperties(parse_mode=ParseMode.HTML),
    )

    return bot


def get_dispatcher(
    routers: list[Router], repository: RepositoryInterface
) -> Dispatcher:
    dp = Dispatcher()

    for router in routers:
        dp.include_router(router)

    dp.shutdown.register(repository.close)

    return dp


def get_text_router(service: ServiceInterface) -> Router:
    return TextRouter(service=service).get_router()


def get_menu_router(service: RagServiceInterface) -> Router:
    return MenuRouter(service=service).get_router()


def get_media_router(service: RagServiceInterface) -> Router:
    return MediaRouter(rag_service=service).get_router()


async def get_vector_db() -> AsyncClientAPI:
    return await chromadb.AsyncHttpClient(host='localhost', port=8000)
