from typing import List
from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.ext.asyncio import AsyncSession

from app.db.base import get_db
from app.schemas.feedback import FeedbackMessage, FeedbackMessageCreate, FeedbackMessageUpdate
from app.crud.feedback import feedback as crud_feedback

router = APIRouter()


@router.post("/", response_model=FeedbackMessage)
async def create_feedback(
    feedback_in: FeedbackMessageCreate,
    db: AsyncSession = Depends(get_db)
):
    """Create a new feedback message"""
    return await crud_feedback.create(db=db, obj_in=feedback_in)


@router.get("/", response_model=List[FeedbackMessage])
async def read_feedbacks(
    skip: int = 0,
    limit: int = 100,
    db: AsyncSession = Depends(get_db)
):
    """Retrieve feedback messages"""
    return await crud_feedback.get_multi(db, skip=skip, limit=limit)


@router.get("/{feedback_id}", response_model=FeedbackMessage)
async def read_feedback(
    feedback_id: int,
    db: AsyncSession = Depends(get_db)
):
    """Get feedback message by ID"""
    feedback = await crud_feedback.get(db=db, id=feedback_id)
    if not feedback:
        raise HTTPException(status_code=404, detail="Feedback not found")
    return feedback


@router.put("/{feedback_id}", response_model=FeedbackMessage)
async def update_feedback(
    feedback_id: int,
    feedback_in: FeedbackMessageUpdate,
    db: AsyncSession = Depends(get_db)
):
    """Update feedback message"""
    feedback = await crud_feedback.get(db=db, id=feedback_id)
    if not feedback:
        raise HTTPException(status_code=404, detail="Feedback not found")
    return await crud_feedback.update(db=db, db_obj=feedback, obj_in=feedback_in)


@router.delete("/{feedback_id}")
async def delete_feedback(
    feedback_id: int,
    db: AsyncSession = Depends(get_db)
):
    """Delete feedback message"""
    feedback = await crud_feedback.get(db=db, id=feedback_id)
    if not feedback:
        raise HTTPException(status_code=404, detail="Feedback not found")
    await crud_feedback.remove(db=db, id=feedback_id)
    return {"message": "Feedback deleted successfully"}