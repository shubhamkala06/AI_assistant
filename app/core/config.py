from functools import lru_cache

from pydantic_settings import BaseSettings, SettingsConfigDict


class AppSettings(BaseSettings):
    app_name: str
    environment: str
    debug: bool = False

    model_config = SettingsConfigDict(env_prefix="", extra="ignore", env_file=".env")


class LoggingSettings(BaseSettings):
    log_level: str = "INFO"

    model_config = SettingsConfigDict(env_prefix="", extra="ignore", env_file=".env")


class Settings:
    def __init__(self) -> None:
        self.app = AppSettings()
        self.logging = LoggingSettings()


@lru_cache
def get_settings() -> Settings:
    return Settings()
