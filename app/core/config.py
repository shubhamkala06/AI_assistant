from functools import lru_cache

from pydantic import Field, computed_field
from pydantic_settings import BaseSettings, SettingsConfigDict


class AppSettings(BaseSettings):
    app_name: str
    environment: str
    debug: bool = False

    model_config = SettingsConfigDict(env_prefix="", extra="ignore", env_file=".env")


class LoggingSettings(BaseSettings):
    log_level: str = "INFO"

    model_config = SettingsConfigDict(env_prefix="", extra="ignore", env_file=".env")


class DatabaseSettings(BaseSettings):
    driver: str = "postgresql+asyncpg"

    host: str
    port: int

    database: str = Field(validation_alias="POSTGRES_DB")

    user: str
    password: str

    echo: bool = False

    pool_pre_ping: bool = True

    model_config = SettingsConfigDict(
        env_prefix="POSTGRES_", extra="ignore", env_file=".env"
    )

    @computed_field
    @property
    def url(self) -> str:
        return (
            f"{self.driver}://"
            f"{self.user}:{self.password}"
            f"@{self.host}:{self.port}"
            f"/{self.database}"
        )


class Settings:
    def __init__(self) -> None:
        self.app = AppSettings()
        self.logging = LoggingSettings()
        self.database = DatabaseSettings()


@lru_cache
def get_settings() -> Settings:
    return Settings()
