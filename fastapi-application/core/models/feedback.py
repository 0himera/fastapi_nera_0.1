from datetime import datetime

from sqlalchemy import String, ForeignKey, DateTime
from sqlalchemy.orm import Mapped, mapped_column, relationship

from core.models import Base, User
from core.models.mixins.int_id_pk import IntIdPkMixin
from core.types.user_id import UserIdType


class Feedback(Base, IntIdPkMixin):
	user_id: Mapped[UserIdType] = mapped_column(ForeignKey("users.id"), nullable=False)
	content: Mapped[str] = mapped_column(String, nullable=False)
	created_at: Mapped[DateTime] = mapped_column(DateTime, default=datetime.utcnow)

	user: Mapped["User"] = relationship("User", back_populates="feedbacks")

