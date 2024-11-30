from typing import AsyncGenerator

from fastapi import APIRouter, HTTPException, Depends
from sqlalchemy.ext.asyncio import AsyncSession

from api.api_v1.fastapi_users_router import current_active_superuser
from core.models import db_helper, User
from core.schemas.feedback import FeedbackCreate, FeedbackRead, FeedbackUpdate
from core.config import settings
from core.crud.feedback import (
    create_feedback,
    get_feedbacks,
    get_feedback,
    delete_feedback,
    update_feedback,
)

router = APIRouter(
    prefix=settings.api.v1.feedbacks,
    tags=["Feedbacks"],
)


async def get_async_db() -> AsyncGenerator[AsyncSession, None]:
    async for session in db_helper.session_getter():
        yield session

# post
@router.post("", response_model=FeedbackRead)
async def feedback_create(
    feedback_data: FeedbackCreate,
    session: AsyncSession = Depends(get_async_db),
    user: User = Depends(current_active_superuser),
):
    feedback = await create_feedback(feedback_data=feedback_data, db=session, user_id=user.id)
    return feedback

# get
@router.get("/{feedback_id}", response_model=FeedbackRead)
async def feedback_get(feedback_id: int, session: AsyncSession = Depends(get_async_db)):
    feedback_ = await get_feedback(db=session, feedback_id=feedback_id)
    if feedback_ is None:
        raise HTTPException(status_code=404, detail="Feedback not found")
    return feedback_

# get all
@router.get("", response_model=list[FeedbackRead])
async def feedbacks_get(
    skip: int = 0,
    limit: int = 10,
    session: AsyncSession = Depends(get_async_db),
):
    return await get_feedbacks(skip=skip, limit=limit, db=session)

# edit
@router.put("/{feedback_id}", response_model=FeedbackRead)
async def feedback_update(
    feedback_id: int,
    feedback_data: FeedbackUpdate,
    session: AsyncSession = Depends(get_async_db),
    user: User = Depends(current_active_superuser),
):
    feedback_ = await get_feedback(db=session, feedback_id=feedback_id)
    if feedback_ is None:
        raise HTTPException(status_code=404, detail="Feedback not found")

    updated_feedback = await update_feedback(
        db=session, feedback_id=feedback_id, feedback_data=feedback_data
    )

    return updated_feedback

# delete
@router.delete("/{feedback_id}", response_model=FeedbackRead)
async def feedback_delete(
    feedback_id: int, session: AsyncSession = Depends(get_async_db),
    user: User = Depends(current_active_superuser),
):
    feedback_ = await delete_feedback(db=session, feedback_id=feedback_id)
    if feedback_ is None:
        raise HTTPException(status_code=404, detail="Feedback not found")
    return feedback_
