from typing import TYPE_CHECKING, List

from fastapi_users_db_sqlalchemy import SQLAlchemyBaseUserTable, SQLAlchemyUserDatabase
from sqlalchemy.orm import Mapped, relationship

from core.types.user_id import UserIdType
from .base import Base
from .mixins.int_id_pk import IntIdPkMixin

if TYPE_CHECKING:
    from .feedback import Feedback  # Импортируйте Feedback только для проверки типов
    from sqlalchemy.ext.asyncio import AsyncSession


class User(Base, IntIdPkMixin, SQLAlchemyBaseUserTable[UserIdType]):
    feedbacks: Mapped[List["Feedback"]] = relationship(
        "Feedback", back_populates="user"
    )

    @classmethod
    def get_db(cls, session: "AsyncSession"):
        return SQLAlchemyUserDatabase(session, cls)
