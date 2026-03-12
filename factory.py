from aiogram import Bot, Dispatcher, Router
from aiogram.client.default import DefaultBotProperties
from aiogram.enums import ParseMode
from pydantic_ai.models import Model
from httpx import AsyncClient
from pydantic_ai.models.mistral import MistralModel
from pydantic_ai.providers.mistral import MistralProvider

from agent.interfaces import AgentInterface
from agent.pydantic_agent import PydanticAgent
from repositories.interfaces import RepositoryInterface
from redis.asyncio import Redis

from repositories.pydantic_ai_repository import RedisRepository
from routers.text_router import TextRouter
from services.chat_service import ChatService
from services.interfaces import ServiceInterface
from core.settings import settings


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


def get_repository() -> RepositoryInterface:
    redis_client = Redis(host=settings.DB_HOST, port=settings.DB_PORT)

    return RedisRepository(redis_client=redis_client)


def get_service(
    agent: AgentInterface, repository: RepositoryInterface
) -> ServiceInterface:
    return ChatService(agent=agent, repository=repository)


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
