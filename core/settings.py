from pydantic_settings import BaseSettings, SettingsConfigDict
from pathlib import Path

BASE_DIR = Path(__file__).parent.parent


class Settings(BaseSettings):
    model_config = SettingsConfigDict(
        env_file=BASE_DIR / ".env", env_file_encoding="utf-8"
    )

    BOT_TOKEN: str
    MISTRAL_API_KEY: str
    LOGFIRE_TOKEN: str
    LOG_FILENAME: str
    DB_HOST: str
    DB_PORT: int
    MEDIA_DIR: Path = BASE_DIR / "media"
    LOG_DIR: Path = BASE_DIR / "logs"


settings = Settings()  # noqa
