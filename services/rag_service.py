from repositories.interfaces import RepositoryInterface
import json


class RagService:
    def __init__(self, settings_repository: RepositoryInterface) -> None:
        self._settings_repository = settings_repository

    async def get_status(self, user_id: int) -> bool:
        raw_settings = await self._settings_repository.load(user_id=user_id)
        settings = json.loads(raw_settings) if raw_settings else {}

        return settings.get("rag_status", False)

    async def toggle(self, user_id: int, value: bool) -> bool:
        raw_settings = await self._settings_repository.load(user_id=user_id)
        settings = json.loads(raw_settings) if raw_settings else {}
        settings["rag_status"] = value

        await self._settings_repository.save(user_id=user_id, item=json.dumps(settings))

        return value
