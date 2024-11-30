from sqlalchemy import delete
from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy.future import select

from core.models.feedback import Feedback
from core.schemas.feedback import FeedbackCreate, FeedbackUpdate


# Асинхронная функция для создания отзыва
async def create_feedback(db: AsyncSession, feedback_data: FeedbackCreate, user_id: int):
    try:
        feedback = Feedback(
            user_id=user_id,
            content=feedback_data.content
        )
        db.add(feedback)
        await db.commit()
        await db.refresh(feedback)
        return feedback

    except Exception as e:
        await db.rollback()  # Откатываем транзакцию при ошибке
        raise e


# Асинхронная функция для получения отзыва по ID
async def get_feedback(db: AsyncSession, feedback_id: int):
    result = await db.execute(select(Feedback).where(Feedback.id == feedback_id))
    return result.scalars().first()


# Асинхронная функция для получения всех отзывов
async def get_feedbacks(db: AsyncSession, skip: int = 0, limit: int = 10):
    result = await db.execute(
        select(Feedback)
        .offset(skip)
        .limit(limit)
    )
    return result.scalars().all()


# Асинхронная функция для обновления отзыва
async def update_feedback(db: AsyncSession, feedback_id: int, feedback_data: FeedbackUpdate):
    result = await db.execute(select(Feedback).where(Feedback.id == feedback_id))
    feedback = result.scalars().first()

    if not feedback:
        return None  # Если отзыв не найден

    # Обновляем поля отзыва
    if feedback_data.content is not None:
        feedback.content = feedback_data.content

    await db.commit()
    await db.refresh(feedback)  # Обновляем объект после коммита
    return feedback


# Асинхронная функция для удаления отзыва
async def delete_feedback(db: AsyncSession, feedback_id: int):
    # Получаем отзыв по ID
    result = await db.execute(select(Feedback).where(Feedback.id == feedback_id))
    feedback = result.scalars().first()

    # Если отзыв существует, удаляем его
    if feedback:
        await db.execute(delete(Feedback).where(Feedback.id == feedback_id))
        await db.commit()
    return feedback
