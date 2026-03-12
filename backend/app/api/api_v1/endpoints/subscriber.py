from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.ext.asyncio import AsyncSession

from app.db.base import get_db
from app.schemas.subscriber import Subscriber, SubscriberCreate
from app.crud.subscriber import subscriber as crud_subscriber

router = APIRouter()


@router.post("/", response_model=Subscriber)
async def create_subscriber(
    subscriber_in: SubscriberCreate,
    db: AsyncSession = Depends(get_db)
):
    """Subscribe to newsletter"""
    # Check if email already exists
    existing_subscriber = await crud_subscriber.get_by_email(db, email=subscriber_in.email)
    if existing_subscriber:
        if existing_subscriber.active:
            raise HTTPException(status_code=400, detail="Email already subscribed")
        # Reactivate existing subscriber
        return await crud_subscriber.update(db, db_obj=existing_subscriber, obj_in={"active": True})
    
    return await crud_subscriber.create(db=db, obj_in=subscriber_in)


@router.get("/{email}", response_model=Subscriber)
async def get_subscriber(
    email: str,
    db: AsyncSession = Depends(get_db)
):
    """Get subscriber by email"""
    subscriber = await crud_subscriber.get_by_email(db, email=email)
    if not subscriber:
        raise HTTPException(status_code=404, detail="Subscriber not found")
    return subscriber


@router.delete("/{email}")
async def unsubscribe(
    email: str,
    db: AsyncSession = Depends(get_db)
):
    """Unsubscribe from newsletter"""
    subscriber = await crud_subscriber.get_by_email(db, email=email)
    if not subscriber:
        raise HTTPException(status_code=404, detail="Subscriber not found")
    
    if not subscriber.active:
        raise HTTPException(status_code=400, detail="Already unsubscribed")
    
    await crud_subscriber.update(db, db_obj=subscriber, obj_in={"active": False})
    return {"message": "Successfully unsubscribed"}