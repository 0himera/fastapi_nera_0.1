from typing import TYPE_CHECKING

from fastapi_users.db import SQLAlchemyBaseUserTable, SQLAlchemyUserDatabase

if TYPE_CHECKING:
	from sqlalchemy.ext.asyncio import AsyncSession

from .base import Base
from .mixins.int_id_pk import IntIdPkMixin


class User(Base, IntIdPkMixin, SQLAlchemyBaseUserTable[int]):

	@classmethod
	def get_db(cls, session: AsyncSession):
		return SQLAlchemyBaseUserTable(session, User)
