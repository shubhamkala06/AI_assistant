from fastapi_users_db_sqlalchemy import SQLAlchemyBaseUserTableUUID
from sqlalchemy.orm import Mapped, relationship

from app.domains.auth.models import OAuthAccount
from app.infrastructure.database.base import Base


class User(SQLAlchemyBaseUserTableUUID, Base):
    __tablename__ = "users"

    oauth_accounts: Mapped[list[OAuthAccount]] = relationship(
        "OAuthAccount",
        lazy="joined",
    )
