from pydantic import BaseModel, EmailStr
from typing import Optional
from datetime import datetime


class FeedbackMessageBase(BaseModel):
    name: str
    email: EmailStr
    phone: Optional[str] = None
    subject: Optional[str] = None
    message: str
    status: Optional[str] = "new"


class FeedbackMessageCreate(FeedbackMessageBase):
    pass


class FeedbackMessageUpdate(BaseModel):
    status: Optional[str] = None
    subject: Optional[str] = None
    message: Optional[str] = None


class FeedbackMessageInDBBase(FeedbackMessageBase):
    id: int
    user_id: Optional[int] = None
    created_at: datetime
    updated_at: datetime

    class Config:
        from_attributes = True


class FeedbackMessage(FeedbackMessageInDBBase):
    pass