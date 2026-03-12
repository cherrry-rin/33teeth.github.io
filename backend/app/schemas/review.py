from pydantic import BaseModel
from typing import Optional
from datetime import datetime


class ReviewBase(BaseModel):
    user_id: int
    appointment_id: Optional[int] = None
    rating: int  # 1-5
    comment: Optional[str] = None


class ReviewCreate(ReviewBase):
    pass


class ReviewInDBBase(ReviewBase):
    id: int
    created_at: datetime

    class Config:
        from_attributes = True


class Review(ReviewInDBBase):
    pass