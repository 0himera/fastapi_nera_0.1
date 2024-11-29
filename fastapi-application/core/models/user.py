from typing import TYPE_CHECKING, List

from fastapi_users_db_sqlalchemy import SQLAlchemyBaseUserTable, SQLAlchemyUserDatabase
from sqlalchemy.orm import Mapped, relationship

from core.types.user_id import UserIdType
from .feedback import Feedback

if TYPE_CHECKING:
	from sqlalchemy.ext.asyncio import AsyncSession

from .base import Base
from .mixins.int_id_pk import IntIdPkMixin


class User(Base, IntIdPkMixin, SQLAlchemyBaseUserTable[UserIdType]):
	feedbacks: Mapped[List["Feedback"]] = relationship("Feedback", back_populates="user")

	@classmethod
	def get_db(cls, session: "AsyncSession"):
		return SQLAlchemyUserDatabase(session, cls)
