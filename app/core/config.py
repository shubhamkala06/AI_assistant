from functools import lru_cache
from urllib.parse import quote_plus

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
        env_prefix="POSTGRES_",
        extra="ignore",
        env_file=".env",
    )

    @computed_field
    @property
    def asyncpg_url(self) -> str:
        return (
            f"{self.driver}://"
            f"{self.user}:{self.password}"
            f"@{self.host}:{self.port}"
            f"/{self.database}"
        )

    @computed_field
    @property
    def psycopg_url(self) -> str:
        user = quote_plus(self.user)
        password = quote_plus(self.password)

        return f"postgresql://{user}:{password}@{self.host}:{self.port}/{self.database}"


class AuthSettings(BaseSettings):
    reset_password_token_secret: str
    verification_token_secret: str

    google_client_id: str
    google_client_secret: str
    oauth_state_secret: str

    access_token_lifetime_seconds: int = 3600
    cookie_name: str = "auth"
    cookie_secure: bool = False
    cookie_samesite: str = "lax"

    model_config = SettingsConfigDict(
        env_prefix="AUTH_",
        extra="ignore",
        env_file=".env",
    )


class Settings:
    def __init__(self) -> None:
        self.app = AppSettings()
        self.logging = LoggingSettings()
        self.database = DatabaseSettings()
        self.auth = AuthSettings()


@lru_cache
def get_settings() -> Settings:
    return Settings()
