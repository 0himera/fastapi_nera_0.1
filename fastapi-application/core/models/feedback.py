from typing import TYPE_CHECKING

from sqlalchemy import ForeignKey, Text, DateTime
from sqlalchemy.orm import Mapped, mapped_column, relationship
from datetime import datetime
if TYPE_CHECKING:
	from . import User
from .base import Base
from .mixins.int_id_pk import IntIdPkMixin


class Feedback(Base, IntIdPkMixin):

	user_id: Mapped[int] = mapped_column(ForeignKey("users.id"), nullable=False)
	content: Mapped[str] = mapped_column(Text, nullable=False)
	created_at: Mapped[DateTime] = mapped_column(DateTime, default=datetime.utcnow)

	# Используйте строковую аннотацию для обратной связи
	user: Mapped['User'] = relationship("User", back_populates="feedbacks")
