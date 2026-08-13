from uuid import UUID

from fastapi_users_db_sqlalchemy import SQLAlchemyBaseOAuthAccountTableUUID
from fastapi_users_db_sqlalchemy.access_token import (
    SQLAlchemyBaseAccessTokenTableUUID,
)
from sqlalchemy import ForeignKey
from sqlalchemy.orm import Mapped, declared_attr, mapped_column

from app.infrastructure.database.base import Base


class AccessToken(SQLAlchemyBaseAccessTokenTableUUID, Base):
    __tablename__ = "access_tokens"

    @declared_attr
    def user_id(cls) -> Mapped[UUID]:
        return mapped_column(
            ForeignKey("users.id", ondelete="CASCADE"),
            nullable=False,
        )


class OAuthAccount(SQLAlchemyBaseOAuthAccountTableUUID, Base):
    __tablename__ = "oauth_accounts"

    @declared_attr
    def user_id(cls) -> Mapped[UUID]:
        return mapped_column(
            ForeignKey("users.id", ondelete="CASCADE"),
            nullable=False,
        )
