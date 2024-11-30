from typing import Optional
from pydantic import BaseModel, ConfigDict


# Базовая модель для отзыва
class FeedbackBase(BaseModel):
    content: str  # Содержимое отзыва


# Модель для создания отзыва
class FeedbackCreate(FeedbackBase):
    pass  # Можно добавить дополнительные поля, если необходимо


# Модель для обновления отзыва
class FeedbackUpdate(FeedbackBase):
    content: Optional[str] = None  # Можно обновить только содержимое отзыва


# Модель для чтения данных отзыва
class FeedbackRead(FeedbackBase):
    id: int  # Идентификатор отзыва
    user_id: int  # Идентификатор пользователя, оставившего отзыв

    model_config = ConfigDict(from_attributes=True)
