from pathlib import Path

from dotenv import load_dotenv
from pydantic import SecretStr
from pydantic_settings import (
    BaseSettings,
    SettingsConfigDict,
)

PROJECT_ROOT = Path(__file__).resolve().parent.parent

load_dotenv(PROJECT_ROOT / ".env", override=True)


class Settings(BaseSettings):
    model_config = SettingsConfigDict(
        env_file=Path(PROJECT_ROOT / ".env"),
        env_file_encoding="utf-8",
        extra="ignore",
    )

    worker_model: str = "openai:gpt-5.4-mini"
    evaluator_model: str = "openai:gpt-5.4-mini"
    pushover_user: SecretStr | None = None
    pushover_token: SecretStr | None = None
    wikipedia_user_agent: str = "sidekick (https://sebastiancastaneda.dev)"


settings = Settings()
